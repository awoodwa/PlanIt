import pandas as pd
import numpy as np
import math
from scipy.spatial import distance

def get_loc(city, state):
    '''
    This function takes zipcode or user inputted location as an input
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

        location = (directory[row]['lat'], directory[row]['lng'])

    except:
        print('Your inputted city and state is not recognized. Please try\
              a neighboring town.')

    return location

    #I don't think we need zipcode after all? I checked the data and there are
    #no repeated cities within a state.

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

    row = directory.loc[directory['lat'] == location[0] and\
        directory['lng'] == location[1]]

    population = directory[row]['population']

    return population

def get_energy_per_cap(state):
    '''
    This function gets the average energy use per capita of a given state.

    Inputs
        state : string of state ID (e.g. AK for Arkansas)

    Outputs
        energy_per_cap :
    '''

    directory = pd.read_csv('filename')

    row = directory.loc[directory['state_id'] == state]

    energy_per_cap = directory[row]['total_energy']

    return energy_per_cap

def get_tot_energy(pop, energy):
    '''
    This function calculates the energy use of a given population size
    based on average energy use in a given state.

    Inputs
        pop : integer value of population size
        energy : energy use per capita

    Outputs
        energy_use : float of energy use
    '''
    #DOES PER CAPITA HAPPEN BY 1000??????
    energy_use = pop * energy

def nearest_solar_station(location):
    '''
    This function finds the nearest neighbor solar collection station.

    Inputs
        location : tuple containing latitude and longitude

    Outputs
        station_id : integer of station ID number
    '''
    solar_directory = pd.read_csv('solar_stations.csv')

    min_dist = math.inf
    min_dist_id = ''

    for index in range(len(solar_directory)):
        solar_loc = (solar_directory[index]['ISH_LAT (dd)'], solar_directory[index]['ISH_LON(dd)'])
        dist = distance.euclidean(location, solar_loc)
        if dist < min_dist:
            min_dist = dist
            min_dist_id = solar_directory[index]['id']
        else:
            pass

    return min_dist_id
        # in order to call the solar data csv call the id.tar.csv????
