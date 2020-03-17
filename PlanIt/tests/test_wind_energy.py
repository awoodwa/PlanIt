import numpy as np
import h5pyd
from .. import wind_energy


wtk = h5pyd.File("/nrel/wtk-us.h5", 'r')
NYC_idx = (1044, 2378)
NYC08_tseries = wind_energy.create_tseries(wtk, NYC_idx)[1]


def test_power_eff():
    '''
    Test function for power_eff. Checks output value is correct and value is
    not outside an exceptable range.
    '''
    x_test = 14.2

    result_cp = wind_energy.power_eff(x_test)

    assert result_cp == 0.22110923757796938, \
        'Result value is not same as expected'
    assert result_cp <= 0.59, \
        'Result value is outside of expected range'


def test_weibull_coeff():
    '''
    Test function for weibull_coeff. Checks the output values are of the
    correct type, and that a only a tuple of 2 values is returned (k and c).
    '''
    result_coeff = wind_energy.weibull_coeff(NYC08_tseries)

    assert isinstance(result_coeff[1], np.float64), \
        'Result shape parameter is not the type expected'
    assert len(result_coeff) == 2, \
        'Number of result coefficients is unexpected'


def test_weibull_pdf():
    '''
    Test function for weibull_pdf. Checks that PDF for a single value is
    correct, and that the total value of the PDF is not > 1.
    '''
    test_windsp = 4.0
    test_k, test_c = (2.095213510638354, 6.873579224294875)

    result_pdf = wind_energy.weibull_pdf(test_windsp, test_k, test_c)

    assert result_pdf <= 0.15, \
        'Result PDF for wind speed is higher than allowed'

    tot_pdf = []
    for i in np.arange(0, 26, 1.0):
        val = wind_energy.weibull_pdf(i, 2.095213510638354, 6.873579224294875)
        tot_pdf.append(val)
    result_total = sum(tot_pdf)

    assert result_total <= 1.0, \
        'Total PDF for all wind speeds in range cannot be > 1.0'


def test_summation():
    '''
    Test function for summation. Checks that output is of the correct type
    and has the correct value.
    '''
    result_summation = wind_energy.summation(NYC08_tseries)

    assert isinstance(result_summation, float), \
        'Result summation value is not of type float'

    assert result_summation <= 133, \
        'Result summation value is higher than expected'


def test_wind_energy_output():
    '''
    Test function for wind_energy_output. Checks that the output is not
    an unexpectedly low value.
    '''

    result_output = wind_energy.wind_energy_output(NYC08_tseries)

    assert result_output >= 7439, \
        'Result energy output is lower than expected'


def test_create_tseries():
    '''
    Test function for create_tseries. Checks that the output is a list
    and the values in the list are numpy array.
    '''
    result_tseries = wind_energy.create_tseries(wtk, NYC_idx)

    assert type(result_tseries) == list, \
        'Time series result type is not of type list'
    assert isinstance(result_tseries[1], np.ndarray), \
        'Time series index is not of the type numpy.ndarray'


def test_aeo_average():
    '''
    Test function for aeo_average. Checks that output (an average) is larger
    than the smallest value in the series that make up the average. Also,
    a check that it is of the right type.
    '''
    result_average = wind_energy.aeo_average(wtk, NYC_idx)

    assert np.all(result_average > NYC08_tseries), \
        'Result AEO average is lower than expected'

    assert isinstance(result_average, float), \
        'Result AEO average is not of type float'


def test_wind_landuse():
    '''
    Test function for wind_landuse. Checks output (max energy), is a float,
    and is not an unexpectedly high number.
    '''
    land_available = 12

    result_max_energy = wind_energy.wind_landuse(land_available, wtk, NYC_idx)

    assert isinstance(result_max_energy, float), \
        'Result max energy is not of type float'

    assert result_max_energy < 231748, \
        'Result max energy is higher than expected'
