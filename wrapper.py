'''
This is the wrapper module!
'''

import location_handling
import energy_use_handling
import wind_energy
import solar_handeling

import pandas as pd
import numpy as np
import altair as alt

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
            res_per_cap = energy_use_handling.get_res_energy_per_cap(state)
            energy_use = household_size * res_per_cap
            energy_goal = (goal/100) * energy_use

        # only solar will be used for residences
        solar = solar_handeling.annual_solar_mean(wtk, dataset_loc[0], dataset_loc[1])
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
        gov_per_cap = energy_use_handling.get_tot_energy_per_cap(state)
        energy_use = pop * gov_per_cap
        energy_goal = (goal/100) * energy_use

        wind = wind_energy.wind_landuse(land_availabe, dataset_loc)
        turbines = round(land_available / 0.4)
        wind_cost = cost_handling.cost_of_wind(turbines)

        solar_raw = solar_handeling.annual_solar_mean(wtk, dataset_loc)
        panels = round(land_available * 1e6 / 1.635481)
        solar = panels * solar_raw
        solar_cost = cost_handling.cost_of_solar(solar_raw) * panels

        solar_panels = []

        for p in range(round(panels/100000)):
            wind_turbines = []
            for t in range(turbines):
                c = cost_handling.cost_of_wind(t) +\
                        cost_handling.cost_of_solar(p * 100000)
                se = p * solar_raw / 1e6
                we = t * wind
                e = se + we
                wind_turbines.append([p * 100000, t, round(c, 2), round(e, 2)])
            solar_panels.append(wind_turbines)

        #data = pd.DataFrame(solar_panels)

        x = range(round(panels/100000))
        y = np.linspace(turbines, 0, round(panels/100000))
        limit = pd.DataFrame({'x':x, 'y':y})

        p, t, = np.meshgrid(range(0, round(panels/100000), range(0, turbines)))
        e = (p*100000*solar_raw/1e6) + (t*wind)
        c = (cost_handling.cost_of_wind(t) +\
                cost_handling.cost_of_solar(p * 100000))/1000000

        data = pd.DataFrame({'Panels': p.ravel(), 'Turbines': t.ravel(),\
                            'e': e.ravel(), 'Cost': c.ravel()})

        alt.data_transformers.disable_max_rows()
        chart = alt.Chart(data2).mark_point().encode(
            alt.X('Panels:Q',
                  scale = alt.Scale(domain = (0, panels/100000),
                                    clamp = True
                                   ),
                  axis = alt.Axis(title = 'Number of Solar Panels (100,000)')
                 ),
            alt.Y('Turbines:Q',
                  scale = alt.Scale(domain = (0, turbines),
                                    clamp = True
                                   ),
                  axis = alt.Axis(title = 'Number of Wind Turbines')
                 ),
            color = alt.Color('e:Q',
                              legend = alt.Legend(title = 'Energy Output (MWh)'),
                             scale = alt.Scale(scheme = 'viridis')),
            tooltip = ['Panels:Q', 'Turbines:Q', 'Cost:N']
        )

        line = alt.Chart(limit).mark_line().encode(
            x = 'x:Q',
            y = 'y:Q',
            color = alt.value('black')
        )
        alt.layer(
            chart, line).configure_axis(grid = False)
