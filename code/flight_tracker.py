# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 19:54:56 2023

@author: Dominik Schwinn
"""
#
import pandas as pd
import numpy as np
#
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
import xyzservices.providers as xyz
import subprocess
import webbrowser
#
###############################################################################
class Tracker(object):
    def __init__(self,
                 api='flightradar',
                 dt=1000,
                 worldmap='esri',
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
        assert worldmap in ['osm','nasa','esri'], "The specified worldmap \'{}\' is not implemented. Please use one of the following ['osm','nasa','esri']".format(worldmap)

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

    def flight_tracking(self,
                        doc):
        """
        

        Parameters
        ----------
        doc : TYPE
            DESCRIPTION.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        """

        #flight column data source
        flight_cds = ColumnDataSource({'icao':[],
                                       'longitude':[],
                                       'latitude':[],
                                       'operator':[],
                                       'aircraft':[],
                                       'origin':[],'destination':[],
                                       'altitude':[],
                                       'x':[],'y':[],
                                       'callsign':[],
                                       'groundSpeed':[],
                                       'heading':[],
                                       'orientation':[],
                                       })

        def convert_geo_coordinates(df):
            """
            converting longitude/latitude coordinates to mercator projection coordinates.
            calculation from: https://wiki.openstreetmap.org/wiki/Mercator

            Parameters
            ----------
            df : TYPE
                DESCRIPTION.

            Returns
            -------
            df : TYPE
                DESCRIPTION.

            """

            r = 6378137 #earth radius
            df['x'] = np.deg2rad(df['longitude']) * r
            df['y'] = np.log(np.tan(np.pi / 4 + np.deg2rad(df['latitude']) / 2)) * r
            return df

        def calculate_ac_orientation(df):
            """
            heading is given in degrees (0-360) using icao definition (clockwise):
                North = 0
                East = 90
                South = 180
                West = 270
            The orientation of the AC in the map later is oriented in mathematical sense (counter-clockwise)
            This function turns the icao-heading into the mathematical orientation

            Parameters
            ----------
            df : TYPE
                DESCRIPTION.

            Returns
            -------
            df : TYPE
                DESCRIPTION.

            """
            df['orientation'] = 360-df['heading']
            # print(" df[:,['heading','orientation']] ".center(80,'*'))
            # print(df.loc[:,['heading','orientation']])
            return df


        def refresh_flight_data():
            """
            calls the Tracker class/instance and gets new data which will then be streamed to bokeh

            Returns
            -------
            None.

            """
            self.x = Tracker(self.api,self.dt)
            df = self.x.ac_df
            df = convert_geo_coordinates(df)
            df = calculate_ac_orientation(df)
            # flight_cds.stream(df.to_dict(orient='list'))
            # len(df) has to be added as inout parameters, otherwise the aircraft's trace will be plotted,
            # i.e. every new position of an AC will be added to the plot --> trace is generated
            flight_cds.stream(df.to_dict(orient='list'),len(df))


        doc.add_periodic_callback(refresh_flight_data, self.dt)
        x_range,y_range=([-18924313.434856508, 18924313.434856508], [-12932243.11199202, 12932243.11199202]) #bounding box
        p=figure(x_range=x_range,y_range=y_range,x_axis_type='mercator',y_axis_type='mercator',sizing_mode='scale_width',height=300)
        doc.title='aviator flight tracking (development)'
        if worldmap == 'osm':
            p.add_tile(xyz.OpenStreetMap.Mapnik)
        if worldmap == 'nasa':
            p.add_tile(xyz.NASAGIBS.ViirsEarthAtNight2012)
        if worldmap == 'esri':
            p.add_tile(xyz.Esri.WorldImagery)
        p.triangle('x','y',source=flight_cds,fill_color='blue',hover_color='red',size=12,#fill_alpha=0.8,line_width=0.1,
                   angle='orientation',angle_units='deg',
                   )

        hover=HoverTool()
        hover.tooltips=[('operator','@operator'),
                        ('aircraft','@aircraft'),
                        # ('origin','@origin'),('destination','@destination'),
                        ('route','{}-{}'.format('@origin','@destination')),
                        ('ground speed','@groundSpeed [kts]'),
                        ('altitude','@altitude [ft]'),
                        ('heading','@heading')]
        p.add_tools(hover)
        doc.add_root(p)


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
        """
        

        Parameters
        ----------
        flights : TYPE, optional
            DESCRIPTION. The default is None.
        verbose : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        None.

        """

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
class OpenSky(object):
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
        print(">>> initializing OpenSky API")


###############################################################################

if __name__ == "__main__":
    # INPUT variables:
    api = 'flightradar' # API to use
    dt = 5000 # update interval of flight data in milliseconds
    port = 9999 # port to use for localhost-application
    worldmap = 'esri' #['osm','esri','nasa']
    #
    x = Tracker(api,
                dt,
                worldmap,
                verbose=False)
    #
    apps = {'/': Application(FunctionHandler(x.flight_tracking))}
    server = Server(apps, port=port) #define an unused port
    server.start()

    subprocess.Popen(['python', '-m', 'SimpleHTTPServer', '{}'.format(port)])
    webbrowser.open_new_tab('http://localhost:{}'.format(port))