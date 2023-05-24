# AVIATOR
AVIATOR is an open-source app related to aviation. It consists of various statistics and visualization tools, based on web scraping (mainly) wikipedia.com. Additionally, it features a simple flight-tracker that runs on a local host.

Currently AVIATOR is under development.

## Flight-tracker
In order to run the flight-tracking app, run the module 'flight_tracker.py' (e.g. in your console) and select the following input parameters at the end of the file:
- api = 'flightradar' (the API which is used to get the airplane data, currently only flightradar is implemented)
- dt = 5000 (the time delta that is used to update the API data)
- port = 9999 (any unused port will do)
- worldmap = 'esri' (alternatively you can use 'osm' or 'nasa', examples see below)

Then your default browser should open automatically showing the corresponding worldmap and the airplanes' movements.

### Flight-tracker using ESRI satellite map (screenshot)
![Flight-tracker using ESRI satellite map](/visualization/aviator_esri.png)
### Detailed flight data (Air India flight BOM-JFK) using ESRI satellite map (screenshot)
Hovering over a triangle highlights the flight in red, showing some flight data. In this example, the operator AI stands for Air India and the flight is from Mumbai (Bombay) to New York (JFK). The aircraft is a Boeing jet 777-200LR/777F (ICAO designation B77L), currently close to Iceland while heading 247° (south-west), with a ground speed of 456 kts at an altitude of 36,000 ft.
![Flight-tracker using ESRI satellite map](/visualization/aviator_esri_detailed_BOM-JFK.png)
### Flight-tracker using OpenStreetMap (screenshot)
![Flight-tracker using OpenStreetMap](/visualization/aviator_osm.png)
### Flight-tracker using NASAGIBS(ViirsEarthAtNight2012) - Map (screenshot)
![Flight-tracker using NASAGIBSMap](/visualization/aviator_nasa.png)

## Visualization tools

## Getting the data
