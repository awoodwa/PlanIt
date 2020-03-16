""" Application configuration - required for running the app"""

import os


class Config:

    SECRET_KEY = os.urandom(25)
    TESTING = True
    DEBUG = True
