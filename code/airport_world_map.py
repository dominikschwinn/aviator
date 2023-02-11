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
        self.airports = pd.read_csv('../data/iata_airport_list.csv')


    def plot_airports_world_map(self,
                                airports=[],
                                savefig=True):
        """
        

        Parameters
        ----------
        airports : TYPE list, optional
            DESCRIPTION. The default is [].
            if airports == []: all airports from 'iata_airports_new.csv' are used (preconditioned they have lat and lon)
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
        fig = plt.gcf()
        plt.show()
        
        if savefig:
            fig.savefig('../visualization/airport_world_map.png',dpi=300)


    def plot_airports_world_map_interactive(self,
                                            airports=[],
                                            savefig=True):
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
            map.save('../visualization/airports_interactive.html', close_file=True)



if __name__ == "__main__":
    x = Visualization()
    x.plot_airports_world_map(airports=[],
                              savefig=True)
    # x.plot_airports_world_map_interactive(airports=['AMS','ATL','ADL','ASU','AUH','ABZ','ANC','AKL'],
                                          # savefig=True)
    x.plot_airports_world_map_interactive(airports=['ATL','SIN','FRA','GIG','LAX','AUH','AMS','DXB','HKG','HND','LHR','JFK','SFO','CDG','SVO','SGN','BKK','DPS',
                                                    'ORD','MAD','CMB','PVG','YYZ','YQB','STR','MUC','DOH'],
                                          savefig=True)