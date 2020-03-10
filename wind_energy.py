import math

import h5pyd
import dateutil
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline  # for power_eff
from pyproj import Proj
from reliability.Fitters import Fit_Weibull_2P  # for weibull_coeff


def power_eff(wind_sp):
    """ Creates turbine wind speed (x) vs power effiency (y) curve based on
    curve from DOI: 10.1016/j.esd.2016.11.001. Outputs y for a given x.

    Parameters
    ----------
    wind_sp: int or float. single wind speed value.

    Return
    ----------
    Cp: int or float. power efficiency value based on inputted wind
    speed
    """
    x = list(np.arange(3, 26.0, 1))
    y = [0.26, 0.35, 0.4, 0.41, 0.425, 0.445, 0.445, 0.425, 0.38, 0.335, 0.28,
         0.23, 0.19, 0.16, 0.13, 0.11, 0.09, 0.075, 0.065, 0.05, 0.04, 0.03,
         0.02]

    cs = CubicSpline(x, y)

    Cp = float(cs(wind_sp))
    return Cp


def weibull_coeff(tseries):
    """ Fits a time series (month, year, decade) of wind speed data with a
    Weibull distribution and returns shape (k) and scale (c) parameter.
    These are needed to calculat the Weibull PDF.

    Parameters
    ----------
    tseries: list, array-like. distrubtion of wind speeds over a given period
    of time.

    Return
    ----------
    k: float. shape parameter, describes the Weibull slope in a probability
    plot.
    c: float. scale parameter, describes height and width of the Weibull
    PDF.
    """
    data = list(tseries)
    wb = Fit_Weibull_2P(failures=data, show_probability_plot=False,
                        print_results=False)
    k = wb.beta
    c = wb.alpha

    return k, c


def weibull_pdf(wind_sp, k, c):
    """ Computes the PDF for a Weibull distribution at a given wind speed,
    with shape and scale parameters calculated from the distrubtion fit.

    Parameters
    ----------
    wind_sp: int or float. single windspeed value.
    k: float. shape parameter, describes the Weibull slope in a probability
    plot.
    c: float. scale parameter, describes height and width of the Weibull
    PDF.

    Return
    ----------
    pdf: int or float. frequency of occurance of an inputted wind speed.
    """
    pdf = (k/c)*(wind_sp/c)**(k-1)*math.exp(-(wind_sp/c)**k)

    return pdf


def summation(tseries):
    """ Sums Cp*wind speed^3* pdf for a range of windspeeds. Prevents
    wind speeds that are too low and too high for wind turbine operation from
    being used to calculate total energy output of wind turbine. Prevents
    powers over the nameplate capacity (max power turbine can intake) from
    being computed.

    Parameters
    ----------
    tseries: list, array-like. distrubtion of wind speeds over a given period
    of time.

    Return
    ----------
    tot_sum: sum of Cp*wind speed^3* pdf over a range of windspeeds, from the
    min to max of the wind speed series.
    """
    summ_list = []
    k, c = weibull_coeff(tseries)

    # incrementing by 1 keeps the PDF at 1
    for wind_sp in np.arange(tseries.min(), tseries.max(), 1.0):
        Cp = power_eff(wind_sp)
        pdf = weibull_pdf(wind_sp, k, c)

        tot_sp = Cp * wind_sp**3
        max_sp = 378  # max wind speed (for max power of turbine) for the
                     # rho and A from turbine specs is 378
                     # 2430 kW = 0.5 * rho * A * Cp * v^3

        # wind must be between 3.5 and 25 m/s for turbine operation
        if wind_sp < 3.5 or wind_sp > 25.0:
            pass
        # for the turbine specs max power 2430 kW.
        # This bit of code makes sure not to account for power over the limit.
        else:
            if tot_sp <= max_sp:
                summ = tot_sp * pdf
            else:
                summ = 378 * pdf

            summ_list.append(summ)

    tot_sum = sum(summ_list)

    return tot_sum


def wind_energy_output(tseries):
    """ Calculates Mega Watt Hours (MWh) per year or Annual Energy Output
    (AEO) of a wind turbine for a given time series of wind data.

    Parameters
    ----------
    tseries: list, array-like. distrubtion of wind speeds over a given period
    of time.

    Return
    ----------
    aeo_mwh: annual energy output in MWh.
    """
    summ = summation(tseries)

    rho = 1.225  # air density
    area = math.pi*(115.6/2)**2  # area of wind turbine blade
    hours_year = 365*24  # hours in a year

    # divide by 1e6 so AEO output is in MWh
    aeo_mwh = (hours_year * 0.5 * rho * area * summ)/1e6

    return aeo_mwh
