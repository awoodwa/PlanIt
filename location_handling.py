import pandas as pd
import numpy as np
import math
import h5pyd
from scipy.spatial import distance

def get_loc(city, state):
    '''
    This function takes city and state as an input
    and returns the longitude and latitude coordinates of that location.

    Inputs
        city : string of city name
        state : string of state ID (e.g. AK for Arkansas)

    Outputs
        location : tuple containing latitude and longitude
    '''
    directory = pd.read_csv('uscities_edit.csv')

    try:
        row = directory.loc[directory['state_id'] == state and\
                      directory['city'] == city]

        return (directory[row]['lat'], directory[row]['lng'])

    except:
        print('Your inputted city and state is not recognized. Please try\
              a neighboring town.')

# def wtk_locator(wtk, loc):
#     '''
#     This function finds the nearest latitude and longitude coordinates in
#     the wind toolkit database.
#
#     Inputs
#         wtk : h5pyd.File instance for the wind toolkit
#         loc : tuple of latitude and longitude coordinates
#
#     Outputs
#         nearest_wtk : tuple of latitude and longitude in database
#     '''
#     coords = wtk['coordinates']
#
#     min_dist = math.inf
#     nearest_wtk = (0, 0)
#
#     for index in range(len(coords)):
#         dist = distance.euclidean(loc, coords[index])
#         if dist < min_dist:
#             min_dist = dist
#             nearest_wtk = (coords[index])
#         else:
#             pass
#
#     return nearest_wtk
#
#
# def nsrdb_locator(nsrdb, loc):
#     '''
#     This function finds the nearest lattitude and longitude coordinates
#     in the NSR database.
#
#     Inputs
#         nsrdb : h5pyd.File instance
#         loc : tuple of latitude and longitude
#
#     Outputs
#         nearest_nsrdb : tuple of latitude and longitude in database
#     '''
#     coords = nsrdb['coordinates'][...]
#
#     min_dist = math.inf
#     nearest_nsrdb = (0, 0)
#
#     for index in range(len(coords)):
#         dist = distance.euclidean(loc, coords[index])
#         if dist < min_dist:
#             min_dist = dist
#             nearest_nsrdb = (coords[index])
#         else:
#             pass
#
#     return nearest_nsrdb
#
#
# def get_ind(file, location):
#     '''
#     This function takes a given latitude and longitude and returns the
#     appropriate index in our dataset.
#
#     Inputs
#         file : h5pyd._h1.files.File type (specific to API usage) that contains
#             desired information
#         location : tuple of latitude and longitude (floats)
#
#     Outputs
#         index : integer value of index in dataset for given location
#     '''


# def get_pop(location):
#     '''
#     This function takes the location and returns the population size of a city
#     or town.
#
#     Inputs
#         location : tuple containing latitude and longitude
#
#     Outputs
#         population : integer
#     '''
#
#     directory = pd.read_csv('uscities_edit.csv')
#
#     row = directory.loc[directory['lat'] == location[0] and\
#         directory['lng'] == location[1]]
#
#     population = directory[row]['population']
#
#     return population
#
#
# def get_energy_per_cap(state):
#     '''
#     This function gets the average energy use per capita of a given state.
#
#     Inputs
#         state : string of state ID (e.g. AK for Arkansas)
#
#     Outputs
#         energy_per_cap :
#     '''
#
#     directory = pd.read_csv('filename')
#
#     row = directory.loc[directory['state_id'] == state]
#
#     energy_per_cap = directory[row]['total_energy']
#
#     return energy_per_cap
#
# def get_tot_energy(pop, energy):
#     '''
#     This function calculates the energy use of a given population size
#     based on average energy use in a given state.
#
#     Inputs
#         pop : integer value of population size
#         energy : energy use per capita
#
#     Outputs
#         energy_use : float of energy use
#     '''
#     #DOES PER CAPITA HAPPEN BY 1000??????
#     energy_use = pop * energy
