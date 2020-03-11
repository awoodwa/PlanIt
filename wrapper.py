'''
This is the wrapper module!
'''

import location_handling
import energy_use_handling
import wind_energy
import solar_handling

import pandas as pd
import h5pyd

# wtk = h5pyd.File('nrel/wtk-us.h5', 'r')

def wrapper(wtk, city, state, land_available, goal = 100, residential = False,\
            energy_bill = 0, household_size = 0):
    '''
    Wrapper function that handles files and user inputs. Default user is
    government.

    Inputs
        wtk : h5 file of data from NREL WTK API
        city : string user input
        state : string user input
        land_avaible : float user input of land available
        residential : boolean; False default
        government : boolean; True default
        energy_bill : float input; 0 default (optional)
        household_size : integer of household size; 0 default (optional)

    Outputs
        energy_output : maximum energy output (kWh)
        panels : number of solar panels (1.6 m^2 each; 160 USD each)
        turbines : number of wind turbines (0.4 km^2 each; 1.3M USD each)
        cost : cost of installation (USD)
    '''
    # return this in addition to table
    user_loc = location_handling.get_loc(city, state)

    # find location in WTK API
    dataset_loc = location_handling.wtk_locator(wtk, user_loc)

    pop = location_handling.get_pop(user_loc)

    if residential:
        # if they input an energy bill we use this
        if energy_bill > 0:
            energy_use = energy_bill
            energy_goal = (goal/100) * energy_use
        # otherwise it defaults to an estimate
        else:
            res_per_cap = energy_use_handling.energy_use_per_cap_res(state)
            energy_use = household_size * res_per_cap
            energy_goal = (goal/100) * energy_use

        # only solar will be used for residences
        solar = solar_handling.annual_solar_mean(wtk, dataset_loc[0], dataset_loc[1])
        # if solar resources are greater than their goal
        if solar >= energy_goal:
            energy_output = energy_goal
            panels = round(energy_goal / (.25 * 8760))
            cost = cost_handling.cost_of_solar(solar) * panels
        # if solar resources fall short
        else:
            energy_output = solar
            panels = round(solar / (.25 * 8760))
            cost = cost_handling.cost_of_solar(solar) * panels

        return [energy_output, panels, cost]

    else:
        # default setting is for government use - grab estimate of energy use
        gov_per_cap = energy_use_handling.energy_use_per_cap_tot(state)
        energy_use = pop * gov_per_cap
        energy_goal = (goal/100) * energy_use

        wind = wind_energy.wind_landuse(land_availabe, dataset_loc)
        turbines = round(land_available / 0.4)
        wind_cost = cost_handling.cost_of_wind(turbines)

        solar_raw = solar_handling.annual_solar_mean(wtk, dataset_loc)
        panels = round(land_available * 1e6 / 1.635481)
        solar = panels * solar_raw
        solar_cost = cost_handling.cost_of_solar(solar_raw) * panels

        data = pd.DataFrame()

        for p in range(panels):
            for t in range(turbines):
                c = cost_handling.cost_of_wind(t) +\
                    cost_handling.cost_of_solar(p)
                se = p * solar_raw
                we = t * wind
                e = se + we
                data[p][t] = {'panels':p, 'turbines':t,
                              'cost':c, 'energy output':e}

        return data 
