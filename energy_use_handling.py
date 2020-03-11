import pandas as pd
import numpy as np


def get_tot_energy_per_cap(state):
    '''
    This function gets the average energy use per capita of a given state.

    Inputs
        state : string of state ID (e.g. AK for Arkansas)

    Outputs
        energy_use : float value in kWh
    '''

    directory = pd.read_csv('SEDS_edit.csv')

    row = directory.loc[(directory['StateCode'] == state) &\
                        (directory['Year'] == 2017) &\
                        (directory['MSN'] == 'TETPB')]

    energy_use_per_cap_tot = row['Data'].values[0] * 293.07107 # convert to kWh

    return energy_use_per_cap_tot


def get_res_energy_per_cap(state):
    '''
    This function gets the average residential energy use per capita
    of a given state.

    Inputs
        state : string of state ID (e.g. AK for Arkansas)

    Outputs
        energy_use : float value in kWh
    '''
    directory = pd.read_csv('SEDS_edit.csv')

    row = directory.loc[(directory['StateCode'] == state) &\
                        (directory['Year'] == 2017) &\
                        (directory['MSN'] == 'TERPB')]

    energy_use = row['Data'].values[0] * 293.07107 # convert to kWh

    return energy_use_per_cap_res


def calc_energy_use(pop, energy):
    '''
    This function calculates the total energy used given a population.
    Can be used for either large scale calculations (for governments) or
    residential calculations (for households) depending on the energy
    input in question.

    Inputs
        pop : integer value of population in question
        energy : float value of energy per capita (either total or
                residential)

    Outputs
        energy_used : float of energy used by a population in kWh
    '''
    energy_used = pop * energy
    return energy_used


def solar_wind_ratio(solar, wind):
    '''
    This function calculates the solar to wind ratio the user should invest
    in.

    Inputs
        solar : float of solar energy that can be harvested in given location
        wind : float of wind energy that can be harvested in given location

    Outputs
        ratio : tuple of ratio values (solar, wind) = solar:wind
    '''
    solar_rat = solar / wind

    ratio = (round(solar_rat, 1), 1)
