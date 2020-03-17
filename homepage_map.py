"""
This script builds the map seen on the homepage of the application
    - there is no reason to run this more than once
"""

import altair
import pandas as pd
from vega_datasets import data

altair.themes.enable("dark")

csv = pd.read_csv("capital_city_energies.csv")
states = altair.topo_feature(data.us_10m.url, feature="states")

csv["Total Energy (kWh)"] = csv["Wind Energy (MWh)"] * 1000
+ csv["Solar Energy (kWh)"]
csv = csv.round(0)


background = altair.Chart(states).mark_geoshape(
    fill="black",
    stroke="white",
    ).properties(
        width=1300,
        height=750
    ).project("albersUsa")
points = altair.Chart(csv).mark_circle(
    color='red',
    size=50,
    opacity=0.6,
    ).encode(
    longitude='Longitude:Q',
    latitude='Latitude:Q',
    size=altair.Size("Total Energy (kWh):Q", title="Total Energy (kWh)"),
    color="Total Energy (kWh):Q",
    opacity=altair.value(0.6),
    tooltip=[
        'State:N', 'Capital:N', 'Wind Energy (MWh):N',
        'Solar Energy (kWh):N', 'Total Energy (kWh):N'],
    )
chart = altair.layer(
    background, points
    ).configure_legend(
    labelFontSize=15,
    titleFontSize=15,
    labelFont="Times New Roman",
    titleFont="Times New Roman",
    ).properties(
    background="none"
    ).configure_view(
    strokeOpacity=0
    )
chart.save('templates/energy.html', embed_options={'renderer': 'svg'})
chart
