# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 19:54:56 2023

@author: Dominik Schwinn
"""
#
import pandas as pd
import numpy as np
#
#
###############################################################################
class Tracker(object):
    def __init__(self,
                 api='flightradar'):

        if api.lower() == 'flightradar':
            self.API = FlightRadar()

###############################################################################  
class FlightRadar(object):
    def __init__(self,
                 verbose=False):

        from FlightRadar24.api import FlightRadar24API
        #https://pypi.org/project/FlightRadarAPI/
        #https://github.com/JeanExtreme002/FlightRadarAPI
        self.fr_api = FlightRadar24API()
        #
###############################################################################

if __name__ == "__main__":
    api = 'flightradar'
    x = Tracker(api)