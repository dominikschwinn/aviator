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
        """
        

        Parameters
        ----------
        api : TYPE (string), optional
            DESCRIPTION. The default is 'flightradar'.

        Returns
        -------
        None.

        """

        self.ac_df = pd.DataFrame()
        self.icao = []
        self.operator = []
        self.aircraft = []
        self.origin = []
        self.destination = []
        self.callsign =[]
        self.latitude = []
        self.longitude = []
        self.altitude = []
        self.category = []
        self.heading = []

        if api.lower() == 'flightradar':
            self.API = FlightRadar(ac_df=self.ac_df,
                                   icao=self.icao,
                                   operator=self.operator,
                                   aircraft=self.aircraft,
                                   origin=self.origin,
                                   destination=self.destination,
                                   callsign=self.callsign,
                                   latitude=self.latitude,
                                   longitude=self.longitude,
                                   altitude=self.altitude,
                                   category=self.category,
                                   heading=self.heading,
                                   )

###############################################################################  
class FlightRadar(object):
    def __init__(self,
                 ac_df=None,
                 icao=None,
                 operator=None,
                 aircraft=None,
                 origin=None,
                 destination=None,
                 callsign=None,
                 latitude=None,
                 longitude=None,
                 altitude=None,
                 category=None,
                 heading=None,
                 verbose=False):
        """
        (Unofficial) flight tracking API
        - https://pypi.org/project/FlightRadarAPI/
        - https://github.com/JeanExtreme002/FlightRadarAPI
        """

        from FlightRadar24.api import FlightRadar24API
        self.fr_api = FlightRadar24API()
        #
###############################################################################

if __name__ == "__main__":
    api = 'flightradar'
    x = Tracker(api)