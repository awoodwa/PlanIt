import pandas as pd
import numpy as np
import math
from scipy.spatial import distance


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

    loc = (row['lat'], row['lng'])

    return loc


def wtk_locator(wtk, loc):
    '''
    This function finds the nearest latitude and longitude coordinates in
    the wind toolkit database.

    Inputs
        wtk : h5pyd.File instance for the wind toolkit
        loc : tuple of latitude and longitude coordinates

    Outputs
        nearest_wtk : tuple of latitude and longitude in database
    '''
    coords = wtk['coordinates']
    c = pd.DataFrame(coords)

    min_dist = math.inf
    nearest_wtk = ()

    for i in range(c.shape[1]):
        for j in range(c.shape[0]):
            check = tuple(c[i][j])
            dist = distance.euclidean(loc, check)
            if dist < min_dist:
                min_dist = dist
                nearest_wtk = check
            else:
                pass

    return nearest_wtk


def nsrdb_locator(nsrdb, loc):
    '''
    This function finds the nearest lattitude and longitude coordinates
    in the NSR database.

    Inputs
        nsrdb : h5pyd.File instance
        loc : tuple of latitude and longitude

    Outputs
        result : list containing the location tuple (latitude and
            longitude) of the nearest input in database and the index
            of that row in the database
                    result[0] = (lat, long)
                    result[1] = index
    '''
    result = []
    coords = nsrdb['coordinates'][...]

    min_dist = math.inf
    nearest_nsrdb = (0, 0)
    idx = 0

    for index in range(len(coords)):
        dist = distance.euclidean(loc, coords[index])
        if dist < min_dist:
            min_dist = dist
            nearest_nsrdb = tuple(coords[index])
            idx = index
        else:
            pass

    result.append(nearest_nsrdb)
    result.append(idx)

    return result


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
