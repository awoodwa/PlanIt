import altair as alt
from vega_datasets import data as data1
import pandas as pd

#print(data.list_datasets())

data = pd.read_csv("capital_city_energies.csv")
#print(data["Capital"])
states = alt.topo_feature(data1.us_10m.url, feature="states")
#print(states)

chart = alt.Chart(data['State']).mark_geoshape(
        fill="darkgray",
        stroke="white",
        ).properties(
            width=800,
            height=500
        ).project("albersUsa")
#chart.save("mapofstates.html")
#chart
data["Total Energy (kWh)"] = data["Wind Energy (MWh)"] * 1000 + data["Solar Energy (kWh)"]
print(data.round(0))