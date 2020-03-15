import numpy as np

import h5pyd

import solar_handling


def test_create_ghi_tseries():
    '''
    This function tests the create_ghi_tseries function. It checks the
    length of the resulting list, the length of the internal lists, and
    the type of the location index input.
    '''
    f = h5pyd.File("/nrel/wtk-us.h5", 'r')
    lansing_idx = (1062, 1938)
    result = solar_handling.create_ghi_tseries(f, lansing_idx)
    actual_length = len(range(2007, 2014))
    year_hours = 8760

    assert len(result) == actual_length,\
        "List of time series not correct length"
    assert len(result[0]) == year_hours,\
        "Individual/yearly time series incorrect length"
    assert type(lansing_idx) is tuple,\
        "Input location index is not a tuple"


def test_annual_solar_energy():
    '''
    This function tests the annual_solar_energy function. It checks the length
    of the resulting list, the type of the values within the list, and the
    type of the location index input.
    '''
    f = h5pyd.File("/nrel/wtk-us.h5", 'r')
    lansing_idx = (1062, 1938)
    result = solar_handling.annual_solar_energy(f, lansing_idx)
    actual_length = len(range(2007, 2014))
    energy_type = np.float64

    assert len(result) == actual_length,\
        "List of energies not correct length"
    assert type(result[0]) is energy_type,\
        "Energy type output is incorrect"
    assert type(lansing_idx) is tuple,\
        "Input location index is not a tuple"


def test_annual_solar_mean():
    '''
    This function tests the annual_solar_mean function. It checks the type of
    the resulting value as well as the type of the location index input.
    '''
    f = h5pyd.File("/nrel/wtk-us.h5", 'r')
    lansing_idx = (1062, 1938)
    result = solar_handling.annual_solar_mean(f, lansing_idx)
    energy_type = np.float64

    assert type(result) is energy_type,\
        "Average energy type output is incorrect"
    assert type(lansing_idx) is tuple,\
        "Input location index is not a tuple"
