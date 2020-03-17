from .. import location_handling
import h5pyd
import numpy as np


def test_get_loc():
    '''
    This function tests the get_loc(city, state) function to make sure the
    output is a tuple containing floats and that the output matches the
    working state output of inputs 'Salem' and 'OR'.
    '''
    test = location_handling.get_loc('Salem', 'OR')
    result = (44.9232, -123.0245)

    assert type(test) == tuple,\
        'Test result type (%s) is not of type tuple.' % str(type(test))

    assert (test[0] == result[0]) & (test[1] == result[1]),\
        'Test result (%s) does not contain expected values (%s).' %\
        (str(test), str(result))


def test_wtk_locator():
    '''
    This function tests the wtk_locator(wtk, location) function to make sure
    the output is a tuple containing integers that match the indices output
    of Salem, OR latitude and longitude coordinates.
    '''
    wtk = h5pyd.File('/nrel/wtk-us.h5', 'r')
    salem = (44.9232, -123.0245)
    test = location_handling.wtk_locator(wtk, salem)
    result = (1320, 480)

    assert type(test) == tuple,\
        'Test result type (%s) is not of type tuple.' % str(type(test))

    assert (test[0] == result[0]) & (test[1] == result[1]),\
        'Test result (%s) does not contain expected values (%s).'\
        % (str(test), str(result))


def test_get_pop():
    '''
    This function tests the get_pop(city, state) function to make sure the
    output is an integer and matches the known value of Salem, OR.
    '''
    salem = (44.9232, -123.0245)
    test = location_handling.get_pop(salem)
    result = np.int64(259816)

    assert type(test) == type(result),\
        'Test result type (%s) is not of type integer.' % str(type(test))

    assert test == result,\
        'Test result (%s) is not equal to expected value.'\
        % (str(test), str(result))
