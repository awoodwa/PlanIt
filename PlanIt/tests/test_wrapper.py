from .. import wrapper
import h5pyd
import altair as alt


def test_wrapper():
    '''
    This function tests the functionality of the wrapper module.
    '''
    wtk = h5pyd.File('/nrel/wtk-us.h5', 'r')
    test_gov =\
        wrapper.wrapper(wtk, 'Salem', 'OR', land_available=20, goal=80)

    assert type(test_gov) == alt.vegalite.v4.api.LayerChart,\
        'Test result type (%s) is not of type (%s).'\
        % (str(test_gov), 'alt.vegalite.v3.api.LayerChart')

    # now to test the residential branch
    test_res =\
        wrapper.wrapper(wtk, 'Salem', 'OR', 100000, goal=100,
                        residential=True, household_size=8)

    result = [149129.03, 307.0, 53454.93, 12144.06, 8.13, 4353.01]

    assert type(test_res) == type(result),\
        'Test result type (%s) is not of type list/array.'\
        % str(type(test_res))

    assert len(test_res) == len(result),\
        'Test result length (%s) is not the expected length (%s).'\
        % (str(len(test_res), len(result)))

    for i in range(6):
        assert test_res[i] == result[i],\
            'Entry in test result list (%s) is not equal to expected result\
            (%s).' % (str(test_res[i]), str(result[i]))
