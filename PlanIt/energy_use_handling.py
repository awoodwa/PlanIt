import pandas as pd


def get_tot_energy_per_cap(state):
    '''
    This function gets the average energy use per capita of a given state.

    Inputs
        state : string of state ID (e.g. AK for Arkansas)

    Outputs
        energy_use : float value in kWh
    '''
    # directory of the energy codes and data by state provided by eia.gov
    directory = pd.read_csv('./data/SEDS_edit.csv')

    # find data of interest - total includes commercial, transportation, etc.
    row = directory.loc[(directory['StateCode'] == state) &
                        (directory['Year'] == 2017) &
                        (directory['MSN'] == 'TETPB')]
    # convert to kWh
    energy_use_per_cap_tot = row['Data'].values[0] * 293.07107

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
    # provided by eia.gov
    directory = pd.read_csv('./data/SEDS_edit.csv')

    # find values of interest - residential instead of total
    row = directory.loc[(directory['StateCode'] == state) &
                        (directory['Year'] == 2017) &
                        (directory['MSN'] == 'TERPB')]
    # convert to kWh
    energy_use_per_cap_res = row['Data'].values[0] * 293.07107

    return energy_use_per_cap_res
