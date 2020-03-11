def cost_of_wind(turbines):
    '''
    This function takes the number of turbines to be installed and
    calculates the cost of installation.

    Inputs
        turbines : integer value of turbines (1.3M USD per turbine)

    Outputs
        cost : float value of dollars
    '''
    cost = turbines * 1.3e6
    return cost


def cost_of_solar(annual_solar_mean):
    '''
    This function calculates the cost of a solar panel installed in a
    given location that has some annual solar intake.

    Inputs
        annual_solar_mean : float of output of solar handling function (kWh)

    Outputs
        cost : float in USD
    '''
    daily_solar = 1000 * annual_solar_mean / 8760 # daily solar power in W
    cost = 3.14 * daily_solar

    return cost
