This folder contains the code that is used in the aviator-project.



### airport_world_map.py
This file contains algorithms to plot airport locations on a world map which are then stored in the folder 'visualization'. Currently two versions are available:
1) a plot as *.png file using geopandas --> plot_airports_world_map()
2) a plot as *.html file using folium --> plot_airports_world_map_interactive()

Both functions require a list as input argument. In case the list is empty, all available airports are plotted. Alternatively, a list with the IATA codes can be submitted to the functions to plot only selected airports on the map.

Below is an example of the airport world map (only selected airports by using the airport_list_02):
![airport_world_map](https://user-images.githubusercontent.com/122737573/220220123-e4bc023b-ea9a-4fce-856c-3543acf6c57f.png)



### airport_data.py
This file contains the web scraping algorithm that was/is used to crawl wikipedia for IATA and ICAO airport codes. Moreover, it tries to open the corresponding wikipedia pages for the airports listed in order to extract additional information (e.g. elevation above sea level of the airport, etc.).
