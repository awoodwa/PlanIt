import math
import h5pyd
import dateutil
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline  # for power_eff
from reliability.Fitters import Fit_Weibull_2P  # for weibull_coeff


def power_eff(wind_sp):
    '''
    This function creates a turbine wind speed (x) vs power effiency (y) 
    curve based on curve from DOI: 10.1016/j.esd.2016.11.001. It outputs Cp for
    a given wind speed.

    Inputs
        wind_sp: float. single wind speed value.

    Outputs
        Cp: float. power efficiency value.
    '''
    x = list(np.arange(3, 26.0, 1))
    y = [0.26, 0.35, 0.4, 0.41, 0.425, 0.445, 0.445, 0.425, 0.38, 0.335, 0.28,
         0.23, 0.19, 0.16, 0.13, 0.11, 0.09, 0.075, 0.065, 0.05, 0.04, 0.03,
         0.02]

    cs = CubicSpline(x, y)

    Cp = float(cs(wind_sp))
    return Cp


def weibull_coeff(tseries):
    '''
    This function fits a time series of wind speed data with a
    Weibull distribution and returns shape (k) and scale (c) parameter.
    These are used to calculate the Weibull PDF.

    Inputs
        tseries: array-like. distrubtion of wind speeds.

    Outputs
        k: float. shape parameter, describes the Weibull slope in a probability
        plot.
        c: float. scale parameter, describes height and width of the Weibull
        PDF.
    '''
    data = list(tseries)
    wb = Fit_Weibull_2P(failures=data, show_probability_plot=False,
                        print_results=False)
    k = wb.beta
    c = wb.alpha

    return k, c


def weibull_pdf(wind_sp, k, c):
    ''' This function computes the PDF for a Weibull distribution at a given
    wind speed, with shape and scale parameters calculated from the distrubtion
    fit.

    Inputs
        wind_sp: float. single windspeed value.
        k: float. shape parameter, describes the Weibull slope in a probability
        plot.
        c: float. scale parameter, describes height and width of the Weibull
        PDF.

    Outputs
        pdf: float. frequency of occurance of an inputted wind speed.
    '''
    pdf = (k/c)*(wind_sp/c)**(k-1)*math.exp(-(wind_sp/c)**k)

    return pdf


def summation(tseries):
    '''
    This function sums Cp*wind speed^3* pdf for a range of windspeeds. It
    also prevents wind speeds that are out of range for wind turbine operation
    from being used to calculate total energy output of wind turbine. Prevents
    powers over the nameplate capacity (max power turbine can intake) from
    being computed.

    Inputs
        tseries: array-like. distrubtion of wind speeds.

    Outputs
        tot_sum: sum of (Cp*wind speed^3* pdf) over a range from the min to
        max of the wind speed series.
    '''
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
    '''
    This function calculates Mega Watt Hours (MWh) per year or Annual
    Energy Output (AEO) of a wind turbine.

    Inputs
        tseries: array-like. distrubtion of wind speeds.

    Outputs
        aeo_mwh: annual energy output in MWh.
    '''
    summ = summation(tseries)

    rho = 1.225  # air density
    area = math.pi*(115.6/2)**2  # area of wind turbine blade
    hours_year = 365*24  # hours in a year

    # divide by 1e6 so AEO output is in MWh
    aeo_mwh = (hours_year * 0.5 * rho * area * summ)/1e6

    return aeo_mwh

def create_tseries(wtk, loc):
    '''
    Creates a list of time series for inputs in other functions.

    Inputs
        wtk : h5pyd file
        loc : tuple of latitude and longitude

    Outputs
        tseries_list : list of tseries for 2007 - 2013
    '''
    # create dset
    dset = wtk['windspeed_100m']

    dt = wtk['datetime']
    dt = pd.DataFrame({'datetime':dt[:]}, index = range(0, dt.shape[0]))
    dt['datetime'] = dt['datetime'].apply(dateutil.parser.parse)

    twenty07 = dt.loc[(dt.datetime >= '2007-01-01') &
                      (dt.datetime < '2008-01-01')].index
    twenty08 = dt.loc[(dt.datetime >= '2008-01-01') &
                      (dt.datetime < '2009-01-01')].index
    twenty09 = dt.loc[(dt.datetime >= '2009-01-01') &
                      (dt.datetime < '2010-01-01')].index
    twenty10 = dt.loc[(dt.datetime >= '2010-01-01') &
                      (dt.datetime < '2011-01-01')].index
    twenty11 = dt.loc[(dt.datetime >= '2011-01-01') &
                      (dt.datetime < '2012-01-01')].index
    twenty12 = dt.loc[(dt.datetime >= '2012-01-01') &
                      (dt.datetime < '2013-01-01')].index
    twenty13 = dt.loc[(dt.datetime >= '2013-01-01') &
                      (dt.datetime < '2014-01-01')].index

    time_slices = [twent07, twenty08, twenty09, twenty10, twenty11, twenty12,
                   twenty13]

    tseries_list = []

    for i in time_slices:
        t = dset[min(i):max(i) + 1, loc[0], loc[1]]
        tseries_list.append(t)

    return tseries_list


def aeo_average(wtk, loc):
    '''
    This function creates the average over all 7 years of wind energy.

    Inputs
        tseries_list : list of time series

    Outputs
        average : average energy over 7 years (MWh)
    '''
    tseries_list = create_tseries(wtk, loc)
    averages = []

    for i in tseries_list:
        averages.append(wind_energy_output(i))

    average = sum(averages)/len(averages)

    return average


def wind_landuse(land_available, tseries_list):
    '''
    This function calculates the maximum power output achieved by wind
    energy alone in a given location with given land availability.

    Inputs
        land_available : float of land free user input in km^2
        tseries_list : output of create_tseries; list of time series

    Outputs
        max_power_output : max power to be harvested in land area
    '''
    # 0.4 km^2/turbine approximately
    num_turbines = land_available / 0.4
    max_power_output = num_turbines * (aeo_average(tseries_list)/8760)

    return max_power_output
