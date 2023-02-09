# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 22:20:54 2023

@author: domin
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# world = gpd.read_file(gpd.datasets.get_path('naturalearth_highres'))
world.explore()

airports = pd.read_csv('../data/iata_airports_new.csv')

gdf = gpd.GeoDataFrame(airports, geometry=gpd.points_from_xy(airports.Longitudes, airports.Latitudes))

# ax = world[world.continent == 'South America'].plot(color='white', edgecolor='black')
ax = world.plot()
# gdf.plot(ax=ax, color='red')
gdf.plot(ax=ax, color='red', markersize=.1)
fig = plt.gcf()
plt.show()
fig.savefig('airports.png',dpi=300)