import energy_use_handling
import numpy as np


def test_get_tot_energy_per_cap():
    '''
    This function tests the get_tot_energy_per_cap(state) function
    to make sure that it is of the correct type and known value for inputs
    'Salem' and 'OR'.
    '''
    test = energy_use_handling.get_tot_energy_per_cap('OR')
    result = np.float64(72945.38932300001)

    assert type(test) == type(result),\
        'Test result type (%s) is not of type float.' % str(type(test))

    assert test == result,\
        'Test result (%s) is not equal to expected value (%s).'\
        % (str(test), str(result))


def test_get_res_energy_per_cap():
    '''
    This function tests the get_res_energy_per_cap(state) function
    to make sure taht it is of the correct type and known value for inputs
    'Salem' and 'OR'.
    '''
    test = energy_use_handling.get_res_energy_per_cap('OR')
    result = np.float64(18668.627159000003)

    assert type(test) == type(result),\
        'Test result type (%s) is not of type float.' % str(type(test))

    assert test == result,\
        'Test result (%s) is not equal to expected value (%s).'\
        % (str(test), str(result))
