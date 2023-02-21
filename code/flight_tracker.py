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
                 api='flightradar',
                 dt=1000,
                 verbose=False):
        """
        

        Parameters
        ----------
        api : TYPE (string), optional
            DESCRIPTION. The default is 'flightradar'.
        dt : TYPE (int), optional
            DESCRIPTION. The default is 1000.
        verbose : TYPE (boolean), optional
            DESCRIPTION. The default is False.

        Returns
        -------
        None.

        """

        self.dt = dt #delta t (update interval in milliseconds)
        self.ac_df = pd.DataFrame()
        self.icao = []
        self.operator = []
        self.aircraft = []
        self.origin = []
        self.destination = []
        self.callsign =[]
        self.groundSpeed = []
        self.latitude = []
        self.longitude = []
        self.altitude = []
        self.category = []
        self.heading = []
        self.api = api.lower()

        if api.lower() == 'flightradar':
            self.API = FlightRadar(ac_df=self.ac_df,
                                   icao=self.icao,
                                   operator=self.operator,
                                   aircraft=self.aircraft,
                                   origin=self.origin,
                                   destination=self.destination,
                                   callsign=self.callsign,
                                   groundSpeed=self.groundSpeed,
                                   latitude=self.latitude,
                                   longitude=self.longitude,
                                   altitude=self.altitude,
                                   category=self.category,
                                   heading=self.heading,
                                   verbose=verbose,
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
                 groundSpeed=None,
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

        self.ac_df=ac_df
        self.icao=icao
        self.operator=operator
        self.aircraft=aircraft
        self.origin=origin
        self.destination=destination
        self.callsign=callsign
        self.groundSpeed=groundSpeed
        self.latitude=latitude
        self.longitude=longitude
        self.altitude=altitude
        self.category=category
        self.heading=heading
        self.verbose=verbose
        #
        from FlightRadar24.api import FlightRadar24API
        self.fr_api = FlightRadar24API()
        #
        self.flights = self.get_flights()
        self.flights_2_df(flights=self.flights)
        #
    def get_flights(self,
                    verbose=False):
        """
        get the flights from Flightradar API

        Parameters
        ----------
        verbose : TYPE (boolean), optional
            DESCRIPTION. The default is False.

        Returns
        -------
        flights : TYPE (object)
            DESCRIPTION.

        """
        flights = self.fr_api.get_flights()
        if verbose:
            print(" current flights ".center(80,'*'))
            print(flights)
        return flights

    def flights_2_df(self,
                     flights=None,
                     verbose=False):

        for f in flights:
            self.icao.append(f.icao_24bit)
            self.operator.append(f.airline_iata)
            self.aircraft.append(f.aircraft_code)
            self.origin.append(f.origin_airport_iata)
            self.destination.append(f.destination_airport_iata)
            self.callsign.append(f.callsign)
            self.groundSpeed.append(f.ground_speed)
            self.latitude.append(f.latitude)
            self.longitude.append(f.longitude)
            self.altitude.append(f.altitude)
            self.heading.append(f.heading)
            

        self.ac_df['icao'] = self.icao
        self.ac_df['operator'] = self.operator
        self.ac_df['aircraft'] = self.aircraft
        self.ac_df['origin'] = self.origin
        self.ac_df['destination'] = self.destination
        self.ac_df['callsign'] = self.callsign
        self.ac_df['groundSpeed'] = self.groundSpeed
        self.ac_df['latitude'] = self.latitude
        self.ac_df['longitude'] = self.longitude
        self.ac_df['altitude'] = self.altitude
        self.ac_df['heading'] = self.heading

###############################################################################

if __name__ == "__main__":
    # INPUT variables:
    api = 'flightradar' # API to use
    dt = 5000 # update interval of flight data in milliseconds
    #
    x = Tracker(api,
                dt,
                verbose=False)
    #
