def test_power_eff():

    x_test = 14.2

    result_cp = power_eff(x)

    assert result_cp == 0.22110923757796938, "wrong val outputted, check func"
    assert isinstance(result_cp, float), "output type incorrect"
    assert result_cp <= 0.59, "value too large, check func or input"


def test_weibull_coeff():

    test_tseries = 
