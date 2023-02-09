# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 22:20:54 2023

@author: domin
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

class Visualization():
    def __init__(self):
        print(">>> initializing Visualization")

    def plot_airports_world_map(self,
                                airports=[],
                                savefig=True):
        # assert type(airports)==list
        
        self.airports = pd.read_csv('../data/iata_airports_new.csv')
        
        if len(airports) == 0:
            pass
        if len(airports) > 0:
            self.airports = self.airports.loc[self.airports['IATA'].isin(airports), ['IATA','Airport','Location','Latitudes','Longitudes']]

        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        # world = gpd.read_file(gpd.datasets.get_path('naturalearth_highres'))
        world.explore()
        
        
        
        gdf = gpd.GeoDataFrame(self.airports, geometry=gpd.points_from_xy(self.airports.Longitudes, self.airports.Latitudes))
        
        # ax = world[world.continent == 'South America'].plot(color='white', edgecolor='black')
        ax = world.plot()
        # gdf.plot(ax=ax, color='red')
        gdf.plot(ax=ax, color='red', markersize=.1)
        fig = plt.gcf()
        plt.show()
        
        if savefig:
            fig.savefig('../visualization/airport_world_map.png',dpi=300)


if __name__ == "__main__":
    x = Visualization()
    x.plot_airports_world_map(airports=['AAA','AZZ'],
                              savefig=True)