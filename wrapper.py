import location_handling
import energy_use_handling
import wind_energy
import solar_handling
import cost_handling

import pandas as pd
import numpy as np
import altair as alt


def wrapper(wtk, city, state, land_available, goal=100, residential=False,
            energy_bill=0, household_size=0):
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
        cost_25 : cost of 25 solar panels (can fit on average roof)
        energy_output_25 : energy output of 25 panels in user's area
        energy_saved : how much energy the user saved with only 25 panels
        layer_chart : Altair chart of options (government only)
    '''
    # return this in addition to table
    user_loc = location_handling.get_loc(city, state)

    # find location in WTK API
    dataset_loc = location_handling.wtk_locator(wtk, user_loc)

    pop = location_handling.get_pop(user_loc)

    if residential:
        # if they input an energy bill we use this
        if energy_bill > 0:
            energy_use = energy_bill * 12
            energy_goal = (goal / 100) * energy_use
        # otherwise it defaults to an estimate
        else:
            res_per_cap = energy_use_handling.get_res_energy_per_cap(state)
            energy_use = household_size * res_per_cap
            energy_goal = (goal/100) * energy_use

        # only solar will be used for residences
        solar = solar_handling.annual_solar_mean(wtk, dataset_loc)

        panels = round(energy_goal/solar)
        cost = round(cost_handling.cost_of_solar(solar) * panels, 2)
        energy_output = round(panels * solar, 2)

        # ~25 panels can fit on the average room
        cost_25 = round(cost_handling.cost_of_solar(solar) * 25, 2)
        energy_output_25 = round(25 * solar, 2)
        energy_saved = round((energy_output_25/energy_use)*100, 2)

        return [energy_output, panels, cost, energy_output_25,
                energy_saved, cost_25]

    else:
        # default setting is for government use - grab estimate of energy use
        gov_per_cap = energy_use_handling.get_tot_energy_per_cap(state)
        energy_use = pop * gov_per_cap
        energy_goal = (energy_use * (goal/100))/1000  # (MWh)

        # grab estimate of wind energy that can be harvested (MWh)
        wind = wind_energy.wind_landuse(land_available, wtk, dataset_loc)
        # calculate turbines that could fit in available space
        turbines = round(land_available / 0.4)

        # calculate the raw solar energy that can be harvested (MWh)
        solar_raw = solar_handling.annual_solar_mean(wtk, dataset_loc)/1000
        # number of panels that can fit (convert to m^2)
        panels = round(land_available * 1e6 / 1.635481)

        # anything below this limit is possible
        # above the limit is not tenable due to land restrictions
        x = range(round(panels/100000))
        y = np.linspace(turbines, 0, round(panels/100000))
        limit = pd.DataFrame({'x': x, 'y': y})

        # create a grid of panels and turbines
        p, t = np.meshgrid(range(0, round(panels/100000)), range(0, turbines))
        # implement energy output (MWh)
        e = (p*100000*solar_raw) + (t*wind)
        # implement cost of installations
        c = np.around((cost_handling.cost_of_wind(t) +
                       cost_handling.cost_of_solar(p * 100000))/1000000, 2)
        # what percent of their goal is met
        gp = np.around((e/energy_goal) * 100, 2)

        # create dataframe of raveled parameters
        data = pd.DataFrame({'Panels': p.ravel(), 'Turbines': t.ravel(),
                            'e': e.ravel(), 'Cost': c.ravel(),
                             'PercentGoal': gp.ravel()})

        # create altair option chart with limit line
        alt.themes.enable('dark')
        alt.data_transformers.disable_max_rows()
        chart = alt.Chart(data).mark_point().encode(
            alt.X('Panels:Q',
                  scale=alt.Scale(domain=(0, panels/100000), clamp=True),
                  axis=alt.Axis(title='Number of Solar Panels (100,000)')),
            alt.Y('Turbines:Q',
                  scale=alt.Scale(domain=(0, turbines), clamp=True),
                  axis=alt.Axis(title='Number of Wind Turbines')),
            color=alt.Color('e:Q',
                            legend=alt.Legend(title='Energy Output (MWh)'),
                            scale=alt.Scale(scheme='viridis')),
            tooltip=['Panels:Q', 'Turbines:Q', 'PercentGoal:N', 'Cost:N'])
        line = alt.Chart(limit).mark_line().encode(x='x:Q', y='y:Q',
                                                   color=alt.value('red'))
        layer_chart = alt.layer(
            chart, line).configure_axis(
                grid=False,
                labelFontSize=20,
                titleFontSize=25,
                labelFont="Times New Roman",
                titleFont="Times New Roman",
            ).properties(
                background='none',
                width=1000,
                height=500,
            ).configure_legend(
                labelFontSize=15,
                titleFontSize=15,
                labelFont="Times New Roman",
                titleFont="Times New Roman",
            )
        layer_chart.save(
            'templates/gov_chart.html', embed_options={'renderer': 'svg'})
        return "chart"
