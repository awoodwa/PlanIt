import altair as alt
import pandas as pd
from vega_datasets import data 

csv = pd.read_csv("capital_city_energies.csv")
states = alt.topo_feature(data.us_10m.url, feature="states") #csv["State"]

csv["Total Energy (kWh)"] = csv["Wind Energy (MWh)"] * 1000 + csv["Solar Energy (kWh)"]
csv = csv.round(0)


background = alt.Chart(states).mark_geoshape(
    fill="black",
    stroke="white",
    ).properties(
        width=800,
        height=500
    ).project("albersUsa")
points = alt.Chart(csv).mark_circle(
    color='red',
    size=50,
    opacity=0.6,
    ).encode(
    longitude='Longitude:Q',
    latitude='Latitude:Q',
    #wind='Wind Energy (MWh):Q',
    #solar='Solar Energy(kWh):Q',
    #size=alt.Size("Total Energy (kWh):Q", title = "Total Energy (kWh)"),
    #color=alt.value('red'),    
    #opacity=alt.value(0.6),
    tooltip=['State:N', 'Capital:N', 'Wind Energy (MWh):N', 'Solar Energy (kWh):N', 'Total Energy (kWh):N'],
    )
chart = (background + points)
chart.save('templates/energy.html', embed_options={'renderer': 'svg'})
chart