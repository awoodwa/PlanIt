import pandas as pd
import numpy as np
import math
from pyproj import Proj


def get_loc(city, state):
    '''
    This function takes city and state as an input
    and returns the longitude and latitude coordinates of that location.

    Inputs
        city : string of city name
        state : string of state ID (e.g. AK for Arkansas)

    Outputs
        loc : tuple of latitude and longitude values
    '''
    directory = pd.read_csv('uscities_edit.csv')

    row = directory.loc[(directory['state_id'] == state) &
                        (directory['city'] == city)]

    loc = (row['lat'].values[0], row['lng'].values[0])

    return loc


def wtk_locator(wtk, location):
    '''
    This function finds the nearest latitude and longitude coordinates in
    the wind toolkit database.

    Inputs
        wtk : h5pyd file
        location : tuple of latitude and longitude coordinates

    Outputs
        tuple(reversed(ij)) : tuple of latitude and longitude indices
    '''
    coordinates = wtk['coordinates']
    projectLcc = Proj('+proj=lcc +lat_1=30 +lat_2=60 \
                    +lat_0=38.47240422490422 +lon_0=-96.0 \
                    +x_0=0 +y_0=0 +ellps=sphere \
                    +units=m +no_defs')

    x_origin, y_origin = reversed(coorinates[0][0])
    origin = projectLcc(x_origin, y_origin)

    lon = location[1]
    lat = location[0]

    coords = projectLcc(lon, lat)

    delta = np.subtract(coords, origin)

    ij = [int(round(x/2000)) for x in delta]

    return tuple(reversed(ij))


def get_pop(location):
    '''
    This function takes the location and returns the population size of a city
    or town.

    Inputs
        location : tuple containing latitude and longitude

    Outputs
        population : integer
    '''

    directory = pd.read_csv('uscities_edit.csv')
    lat = location[0]
    lng = location[1]

    row = directory.loc[(directory['lat'] == lat) &
                        (directory['lng'] == lng)]

    population = row['population'].values[0]

    return population
