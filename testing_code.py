import altair as alt
from vega_datasets import data

#print(data.list_datasets())

weather = data.us_state_capitals()
print(weather)

air = data.airports()
print(air)