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


def cost_of_solar(panels):
    '''
    This function takes the number of panels to be installed and
    calculates the cost of the installation.

    Inputs
        panels : integer value of solar panels (160 USD per 1.6 m^2 panel)

    Outputs
        cost : float value of dollars
    '''
    cost = panels * 160
    return cost 
