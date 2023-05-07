# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 22:20:54 2023

@author: Dominik Schwinn
"""

import geopandas as gpd
import folium
import pandas as pd
import matplotlib.pyplot as plt

class Visualization():
    def __init__(self):
        print(">>> initializing Visualization")
        # self.airports = pd.read_csv('../data/iata_airports_new.csv')
        # basic plots:
        # self.airports = pd.read_csv('../data/iata_airport_list.csv')
        #enhanced plots:
        self.airports = pd.read_csv('../data/airport_list_with_stats.csv')
        # print(" self.airports ".center(80,'*'))
        # print(self.airports)


    def plot_airport_map_basic(self,
                                airports=[],
                                savefig=True):
        """
        

        Parameters
        ----------
        airports : TYPE list, optional
            DESCRIPTION. The default is [].
            if airports == []: all airports from 'airport_list_with_stats.csv' are used (preconditioned they have lat and lon)
            if len(airports) != 0: only the specified airports are plotted on the map
            entries in airports must be IATA-code
            e.g. airports = [] or airports = ['AAA','AAZ']
        #
        savefig : TYPE boolean, optional
            DESCRIPTION. The default is True.
        savefig == False: map is only plotted but not saved
        savefig == True: map is plotted and saved as *.png

        Returns
        -------
        None.

        """
        # assert type(airports)==list
        

        
        if len(airports) == 0:
            pass
        if len(airports) > 0:
            self.airports = self.airports.loc[self.airports['IATA'].isin(airports), ['IATA','Airport','Location','Country','Latitudes','Longitudes']]

        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        world.explore()

        gdf = gpd.GeoDataFrame(self.airports, geometry=gpd.points_from_xy(self.airports.Longitudes, self.airports.Latitudes))
        # ax = world[world.continent == 'South America'].plot(color='white', edgecolor='black')
        ax = world.plot()
        gdf.plot(ax=ax, color='red', markersize=.1)
        plt.title("Airport map",fontsize=10)
        plt.xlabel("Longitude [°]")
        plt.ylabel("Latitude [°]")
        plt.grid(True,ls='dotted',lw=0.25)
        fig = plt.gcf()
        plt.show()
        
        if savefig:
            fig.savefig('../visualization/airport_map.png',dpi=300)


    def plot_airport_map_enhanced(self,
                         airports=[],
                         type_='PAX',
                         savefig=True):
        """
        

        Parameters
        ----------
        airports : TYPE, optional
            DESCRIPTION. The default is [].
        type_ : TYPE, optional
            DESCRIPTION. The default is 'PAX'.
        savefig : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None.

        """

        assert type_ in  ['PAX','OPs','Cargo']

        if len(airports) == 0:
            pass
        if len(airports) > 0:
            self.airports = self.airports.loc[self.airports['IATA'].isin(airports), ['IATA','Airport','Location','Country','Latitudes','Longitudes','PAX','OPs','Cargo','Year']]


        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        world.explore()

        # gdf = gpd.GeoDataFrame(self.airports, geometry=gpd.points_from_xy(self.airports.Longitudes, self.airports.Latitudes))

        airport_detailed = self.airports.loc[self.airports[type_].notna()]#.values

        gdf = gpd.GeoDataFrame(airport_detailed, geometry=gpd.points_from_xy(airport_detailed.Longitudes, airport_detailed.Latitudes))

        print(" airport_detailed ({}) ".format(type_))
        print(airport_detailed)
        # pax = airport_pax['PAX'].values.astype(int)
        # print("pax")
        # print(pax)
        # pax_min, pax_max = pax.min(), pax.max()
        # #normalizing pax
        # marker_size = (pax - pax_min) / (pax_max - pax_min)
        # print("marker_size")
        # print(marker_size)
        gdf = gpd.GeoDataFrame(airport_detailed, geometry=gpd.points_from_xy(airport_detailed.Longitudes, airport_detailed.Latitudes))



        ax = world.plot()
        gdf.plot(ax=ax, color='red', markersize=airport_detailed[type_].values.astype(int)/(5*1e6),
                 facecolor='None')
        plt.title("Airport map ({})".format(type_),fontsize=10)
        plt.xlabel("Longitude [°]")
        plt.ylabel("Latitude [°]")
        plt.grid(True,ls='dotted',lw=0.25)
        fig = plt.gcf()
        plt.show()
        
        if savefig:
            fig.savefig('../visualization/airport_map_enhanced_{}.png'.format(type_),dpi=300)        


    def plot_airport_map_basic_interactive(self,
                                            airports=[],
                                            savefig=True):
        """
        

        Parameters
        ----------
        airports : TYPE, optional
            DESCRIPTION. The default is [].
        savefig : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None.

        """
        if len(airports) == 0:
            airport_df = self.airports
        if len(airports) > 0:
            airport_df = self.airports.loc[self.airports['IATA'].isin(airports), ['IATA','Airport','Location','Country','Latitudes','Longitudes']]

        airport_df = airport_df.loc[~airport_df.Latitudes.isna()]
        map = folium.Map(location=[airport_df.Latitudes.mean(), airport_df.Longitudes.mean()], 
                         zoom_start=3, control_scale=True)
        
        for i,row in airport_df.iterrows():
            # folium.Marker(location=[row['Latitudes'],row['Longitudes']]).add_to(map)
            folium.Marker(location=[row['Latitudes'],row['Longitudes']],
                          tooltip=row['Airport'],
                          # popup='{}\n{}'.format(row['Location'],row['Country'])
                          ).add_to(map)

        # map.show_in_browser()
        if savefig:
            map.save('../visualization/airport_map_interactive.html', close_file=True)



if __name__ == "__main__":
    x = Visualization()
    airport_list_01 = ['AMS','ATL','ADL','ASU','AUH','ABZ','ANC','AKL']
    airport_list_02 = ['ATL','SIN','FRA','GIG','LAX','AUH','AMS','DXB','HKG','HND','LHR','JFK','SFO','CDG',
                       'SVO','SGN','BKK','DPS','ORD','MAD','CMB','PVG','YYZ','YQB','STR','MUC','DOH']

    # x.plot_airport_map(airports=[],
    #                           savefig=True)
    # x.plot_airport_map_basic(airports=airport_list_02,
    #                          savefig=False)
    x.plot_airport_map_enhanced(airports=airport_list_02,
                                type_='Cargo',
                                savefig=True)

    # x.plot_airport_map_interactive(airports=[],
    #                                        savefig=True)
    # x.plot_airport_map_basic_interactive(airports=airport_list_02,
    #                                      savefig=True)
    # x.plot_airport_map_interactive(airports=['ATL','SIN','FRA','GIG','LAX','AUH','AMS','DXB','HKG','HND','LHR','JFK','SFO','CDG','SVO','SGN','BKK','DPS',
    #                                                 'ORD','MAD','CMB','PVG','YYZ','YQB','STR','MUC','DOH'],
    #                                       savefig=True)