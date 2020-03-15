""" Application configuration """

import os


class Config:

    SECRET_KEY = os.urandom(25)
    TESTING = True
    DEBUG = True
