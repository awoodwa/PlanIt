# Data

Within this directory, you will find any .csv files that we used in the app as directories to interface with the API.

- uscities_edit.csv contains city and state ID codes and corresponding latitude and longitude coordinates; used in location_handling.get_loc(city, state)
- SEDS_edit.csv contains state, MSN codes (TERPB or total residential energy per capita, and TETPB or total energy per capita), and year; used in energy_use_handling.py functions to estimate energy use per capita in a given state
- capital_city_energy.csv contains data we produced in order to create the homepage interactive map with estimated solar and wind energy values for a single panel and turbine (respectively) in that area
