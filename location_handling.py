import pandas as pd
import numpy as np
import math


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


def wtk_locator(wtk, loc):
    '''
    This function finds the nearest latitude and longitude coordinates in
    the wind toolkit database.

    Inputs
        wtk : h5pyd file
        loc : tuple of latitude and longitude coordinates

    Outputs
        nearest_wtk : tuple of latitude and longitude in database
    '''
    coords = wtk['coordinates']
    c = pd.DataFrame(coords)

    min_dist = math.inf
    nearest_wtk = ()
    index = (0, 0)

    for i in range(c.shape[0]):
        for j in range(c.shape[1]):
            check = c[i][j]
            dist = ((check[0]-loc[0])**2 +(check[1]-loc[1])**2)
            if dist < min_dist:
                min_dist = dist
                nearest_wtk = check
                index = (i, j)
            else:
                pass

    return index


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
