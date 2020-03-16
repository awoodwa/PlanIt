import cost_handling


def test_cost_of_wind():
    '''
    This function tests the cost_of_wind(turbines) function to make sure that
    the result is of the correct type and matches the known value for 3
    turbines.
    '''
    test = cost_handling.cost_of_wind(3)
    result = 3900000.0

    assert type(test) == type(result),\
        'Test result type (%s) is not of type float.' % str(type(test))

    assert test == result,\
        'Test result (%s) is not equal to expected value (%s).'\
        % (str(test), str(result))


def test_cost_of_solar():
    '''
    This function tests the cost_of_solar(annual_solar_mean) function to
    make sure that the result is of the correct type and matches the known
    value for 13,000 kWh as input.
    '''
    test = cost_handling.cost_of_solar(13000)
    result = 4659.817351598173

    assert type(test) == type(result),\
        'Test result type (%s) is not of type float.' % str(type(test))

    assert test == result,\
        'Test result (%s) is not equal to expected value (%s).'\
        % (str(test), str(result))
