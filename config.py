""" Application configuration """
#from os import environ
#import redis
import os


class Config:

    SECRET_KEY = os.urandom(25)
    TESTING = True
    DEBUG = True
