import altair as alt
from vega_datasets import data


def states():
    states = alt.topo_feature(data.us_10m.url, feature="states")
    capitals = data.us_state_capitals()

    background = alt.Chart(states).mark_geoshape(
        fill="darkgray",
        stroke="white",
        ).properties(
            width=800,
            height=500
        ).project("albersUsa")

    points = alt.Chart(capitals).mark_point().encode(
        longitude='lon:Q',
        latitude='lat:Q',
        size=alt.value(15),
        color=alt.value('#3377B3'),
        tooltip=['lon:N', 'lat:N', 'state:N', 'city:N'],
        )

    chart = (background + points)
    chart.save('templates/states.html', embed_options={'renderer': 'svg'})
    chart
