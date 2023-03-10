# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 12:07:49 2023

@author: Dominik Schwinn
"""
import requests
import pandas as pd
import timeit
import re


class Airports(object):
    def __init__(self):
        """
        initializes the Airports class and provides the url-main path

        Returns
        -------
        None.

        """
        self.t_start = self.set_start_time()
        self.url_main_path = f"https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:_"
        # self.r = requests.get(url, headers=HEADERS)
        # print(self.r.text)
        self.HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}


    def set_start_time(self):
        t_start = timeit.default_timer()
        return t_start


    def set_end_time(self):
        t_end = timeit.default_timer()
        return t_end


    def calculate_runtime(self,
                          t_start,
                          t_end,
                          verbose=True):
        runtime = t_end - t_start
        if verbose:
            print("".center(80,'*'))
            print("Runtime: {} [s]".format(runtime))


    def get_url_site(self,
                     str_="A",
                     verbose=True):
        """
        puts together the url that is used for data extraction / web scraping

        Parameters
        ----------
        str_ : TYPE, optional
            DESCRIPTION. The default is "A".

        Returns
        -------
        None.

        """
        self.url = self.url_main_path + str_
        if verbose:
            print("self.url: {}".format(self.url))
            # input("hit a key to continue")


    def read_url_site(self):
        """
        web scraping: reads the url and stores the content in an object
        (type requests.models.Response)

        Returns
        -------
        None.

        """
        self.r = requests.get(self.url, headers=self.HEADERS)
        # print(self.r.text)


    def extract_iata_code(self,
                          elem,
                          verbose=True):
        """
        extracts the iata code frome the airport-data-list element

        Parameters
        ----------
        elem : TYPE
            DESCRIPTION.

        Returns
        -------
        iata : TYPE
            DESCRIPTION.

        """
        iata = elem[0].split('<td>')[1]
        if verbose:
            print("iata: {}".format(iata))
        return iata


    def extract_icao_code(self,
                          elem,
                          verbose=True):
        """
        extracts the icao code frome the airport-data-list element

        Parameters
        ----------
        elem : TYPE
            DESCRIPTION.

        Returns
        -------
        icao : TYPE
            DESCRIPTION.

        """
        icao = elem[1].split('<td>')[1]
        if verbose:
            print("icao:",icao)   
        return icao


    def extract_airportName(self,
                            elem,
                            verbose=True):
        """
        extracts the airport name form the airport-data-list element

        Parameters
        ----------
        elem : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # print("elem[2]:",elem[2])
        elem[2] = elem[2].split("<td>")[1]
        # print("elem[2]:",elem[2])
        # if "</a>" in elem[2]:
        #     airport = elem[2].split("\""">")[1].split("<")[0]
        # else:
        #     airport = elem[2].split("<td>")[1]
        if "<a" in elem[2] and "</a>" in elem[2]:
            m = re.search('>(.+?)</a>', elem[2])
            if m:
                # print(m.group(1))
                airport = m.group(1)
            else:
                airport = ''
        elif "<td>" in elem[2]:
            airport = elem[2].split("<td>")[1]
        else:
            airport = elem[2]#.split("<td>")[1]

        if verbose:
            print("airport name: {}".format(airport))
        return airport


    def extract_location(self,
                         elem,
                         verbose=True):
        """
        extracts the location form the airport-data-list element

        Parameters
        ----------
        elem : TYPE
            DESCRIPTION.

        Returns
        -------
        location : TYPE
            DESCRIPTION.

        """
        elem[3] = elem[3].split("<td>")[1]
        loc = []
        location = ''
        country = ''
        try:
            if ", " in elem[3]:
                l = elem[3].split(", ")
                number_of_locations = len(l)
                # print("l:", l)
                for i, elem in enumerate(l):
                    # print("elem:",elem)
                    if "<a" in elem and "</a>":
                        m = re.search('>(.+?)</a>', elem)
                        if m:
                            print(m.group(1))
                            loc_ = m.group(1)
                        else:
                            loc_ = ''
                        # print("loc_:", loc_)
                    elif "<a" in elem and "</a>" not in elem:
                        pass
                    elif "<a" not in elem and "</a>" in elem:
                        m = re.search('>(.+?)</a>', elem)
                        if m:
                            print(m.group(1))
                            loc_ = m.group(1)
                        else:
                            loc_ = elem
                        # print("loc_:", loc_)
                    else:
                        loc_ = elem
                        # print("loc_:", loc_)
                    if loc_ != '':
                        loc.append(loc_)
                if len(loc) > 1:
                    for i, elem in enumerate(loc[:-1]):
                        # print(i,elem)
                        if i < len(loc) - 2:
                            location += '{}, '.format(elem)
                        elif i == len(loc) - 2:
                            location += '{}'.format(elem)
                    country = '{}'.format(loc[-1])
            else:
                if "<a" in elem[3] and "</a>" in elem[3]:
                    m = re.search('>(.+?)</a>', elem[3])
                    # print(m)
                    location = m.group(1)
                    loc = elem[3].split("</a>")[-2]
                    loc = loc.split(">")[-1]
                    # print("loc:", loc)
                    location, country = location, loc
        except:
            pass

        if verbose:
            print("location: {}".format(location))
            print("country: {}".format(country))

        return location, country


    def extract_utc(self,
                    elem,
                    verbose=True):
        """
        extracts the utc-time zone form the airport-data-list element

        Parameters
        ----------
        elem : TYPE
            DESCRIPTION.

        Returns
        -------
        utc : TYPE
            DESCRIPTION.

        """
        try:
            utc = elem[4].split("\""">")[1].split("</a>")[0]
        except:
            utc = ""
        if verbose:
            print("utc: {}".format(utc))
        return utc


    def get_data_length(self,
                        data,
                        verbose=True):
        """
        get the length of the data array, i.e. how many airport entries are available
        in the Response-object

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        len_data = len(data)
        if verbose:
            print("The Response-object has {} entries".format(len_data))
        return len_data


    def get_airport_data(self,
                         details=False,
                         verbose=True):
        """
        extracts the airport data from the Response-object

        Returns
        -------
        None.

        """
        # if details:
        self.details = details
        data = self.r.text.split("<tr>")
        #ignoring the first two line since they are not relevant (i.e.filled with data)
        data = data[2:]
        len_data = self.get_data_length(data)



        for i,elem in enumerate(data):
            print("=============")
            elem = elem.split('</td>')
            iata = self.extract_iata_code(elem)
            icao = self.extract_icao_code(elem)
            airportName = self.extract_airportName(elem)
            location, country = self.extract_location(elem)
            utc = self.extract_utc((elem))
            
            if self.details:
                airportURL = self.create_airportURL(airport=airportName)
                a = self.read_airportURL_site(airportURL=airportURL)
                if a != None:
                    self.AirportURL.append(airportURL)
                else:
                    self.AirportURL.append(None)
                # if a != N1one:
                lat, lon = self.get_airport_geo_details(a=a)
                elevationUS, elevationSI = self.get_airport_elevation(a=a)
                pax, operations, cargo, year = self.get_airport_statistics(a=a)
            else:
                lat, lon = None, None
                elevation = None
            self.Latitudes.append(lat)
            self.Longitudes.append(lon)
            self.Elevation.append(elevationUS)
            #
            self.PAX.append(pax)
            self.Operations.append(operations)
            self.Cargo.append(cargo)
            self.Year.append(year)

            self.IATA.append(iata)
            self.ICAO.append(icao)
            self.AirportNames.append(airportName)
            self.Locations.append(location)
            self.Countries.append(country)
            self.UTC.append(utc)




    def create_empty_airport_database_columns(self):
        self.IATA = []
        self.ICAO = []
        self.AirportNames = []
        self.Locations = []
        self.Countries = []
        self.UTC = []
        self.Latitudes = []
        self.Longitudes = []
        self.Elevation = []
        self.AirportURL = []
        #
        self.PAX = []
        self.Operations = []
        self.Cargo = []
        self.Year = []
        

    def create_airport_dataframes(self,
                                 verbose=True):
        self.airport_DF = pd.DataFrame()
        self.airport_DF['IATA'] = self.IATA
        self.airport_DF['ICAO'] = self.ICAO
        self.airport_DF['Airport'] = self.AirportNames
        self.airport_DF['Location'] = self.Locations
        self.airport_DF['Country'] = self.Countries
        self.airport_DF['UTC'] = self.UTC
        self.airport_DF['Latitudes'] = self.Latitudes
        self.airport_DF['Longitudes'] = self.Longitudes
        self.airport_DF['Elevation'] = self.Elevation
        self.airport_DF['URL'] = self.AirportURL
        # self.df = df
        self.airport_stats_DF = pd.DataFrame()
        self.airport_stats_DF['IATA'] = self.IATA
        self.airport_stats_DF['PAX'] = self.PAX
        self.airport_stats_DF['OPs'] = self.Operations
        self.airport_stats_DF['Cargo'] = self.Cargo
        self.airport_stats_DF['Year'] = self.Year


    def export_dataframe_2_csv(self,
                             df="None",
                             file_="None",
                             verbose=True,
                             ):
        """
        saves dataframe to csv-file

        Parameters
        ----------
        df : TYPE, optional
            DESCRIPTION. The default is df                             file_=file_.
        verbose : TYPE, optional
            DESCRIPTION. The default is True.
         : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        df.to_csv(file_, index=False)
        if verbose:
            print("DataFrame \"{}\" successfully exported to {}".format(df,file_))


    def create_airportURL(self,
                           airport=None,
                           verbose=True):
        """
        creates the wikipedia url of the specifi

        Parameters
        ----------
        verbose : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None.

        """
        
        url = 'https://en.wikipedia.org/wiki/'
        airportURL = url + airport.replace(' ','_')
        if verbose:
            print("airportURL: {}".format(airportURL))
        return airportURL


    def read_airportURL_site(self,
                             airportURL=None,
                             verbose=True):
        try:
            a = requests.get(airportURL, headers=self.HEADERS)
        except:
            a = None
        return a 
        

    def get_airport_geo_details(self,
                                a=None,
                                verbose=True):
        """
        

        Parameters
        ----------
        airport : TYPE
            DESCRIPTION.
        verbose : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None.

        """
        lat, lon = None,None
        # if verbose:
            # print("airportURL: {}".format(airportURL))
        # try:
        if a != None and "Coordinates" in a.text:
            data = a.text.split('Coordinates')
            # print(data[1][:100])
            m = re.search('{(.+?)}', data[1])
            if m:
                # print(m.group(1))
                geo_data = m.group(1)
                # print("geo_data:",geo_data)
                geo = geo_data.split(',')
                for elem in geo:
                    if "lat" in elem:
                        lat = elem.split(":")[1]
                    if "lon" in elem:
                        lon = elem.split(":")[1]
            # except:
            #     pass
        return lat, lon
                

    def get_airport_elevation(self,
                              a=None,
                              verbose=True):
        """
        

        Parameters
        ----------
        a : TYPE, optional
            DESCRIPTION. The default is a.
        verbose : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None.

        """
        elevationUS, elevationSI = None, None
        if a != None and "Elevation" in a.text:
            try:
                data = a.text.split('Elevation')
                # print(data[1][:200])
                data = data[1].split("infobox-data\">")[1]
                # print("data:",data)
                elevation = data.split("</td>")[0].split(' / ')
                # print("elevation:",elevation)
                elevationUS = elevation[0].split('\xa0ft')[0]
                elevationSI = elevation[1].split('\xa0m')[0]
            except:
                pass

        return elevationUS, elevationSI



    def get_airport_statistics(self,
                               a=None):
        pax, am, cargo, year = None, None, None, None
        if a != None and 'Statistics' in a.text:
            try:
                data = a.text.split('Statistics (')
                year = data[1][:4]#.split(')')[0]
                year = int(year)
                print("statistics from year: ",year)
                # print(data[1][:300])
                if 'Passengers' in data[1]:
                    pax = data[1].split('Passengers')
                    pax = pax[1][:300]
                    pax = re.search('<td class="infobox-data">(.+?)</td>', pax)
                    pax = pax.group(1)
                    if ',' in pax:
                        pax = pax.replace(',','')
                    pax = int(pax)
                    print("pax:", pax)
                if 'Passenger volume' in data[1]:
                    pax = data[1].split('Passenger volume')
                    pax = pax[1][:300]
                    pax = re.search('<td class="infobox-data">(.+?)</td>', pax)
                    pax = pax.group(1)
                    if ',' in pax:
                        pax = pax.replace(',','')
                    pax = int(pax)
                    print("pax:", pax)
                if 'Aircraft Movements' in data[1]:
                    am = data[1].split('Aircraft Movements')
                    am = am[1][:300]
                    am = re.search('<td class="infobox-data">(.+?)</td>', am)
                    am = am.group(1)
                    if ',' in am:
                        am = am.replace(',','')
                    am = int(am)
                    print("aircraft movements:", am)
                if 'Movements' in data[1]:
                    am = data[1].split('Movements')
                    am = am[1][:300]
                    am = re.search('<td class="infobox-data">(.+?)</td>', am)
                    am = am.group(1)
                    if ',' in am:
                        am = am.replace(',','')
                    am = int(am)
                    print("(aircraft) movements:", am)
                if 'Aircraft operations' in data[1]:
                    am = data[1].split('Aircraft operations')
                    am = am[1][:300]
                    am = re.search('<td class="infobox-data">(.+?)</td>', am)
                    am = am.group(1)
                    if ',' in am:
                        am = am.replace(',','')
                    am = int(am)
                    print("aircraft movements (operations):", am)
                if 'Cargo' in data[1]:
                    cargo = data[1].split('Cargo')
                    cargo = cargo[1][:300]
                    cargo = re.search('<td class="infobox-data">(.+?)</td>', cargo)
                    cargo = cargo.group(1)      
                    if ',' in cargo:
                        cargo = cargo.replace(',','')
                    cargo = int(cargo)
                    print("cargo:",cargo)
                # input("found some statistics")
            except:
                pass
        return pax, am, cargo, year


    def clean_data(self,
                   df=None,
                   columns=[],
                   verbose=True):
        print(">>> cleaning columns {} of dataFrame {}".format(columns,df))


if __name__ == "__main__":
    a = Airports()
    a.create_empty_airport_database_columns()
    # for letter in ["Z"]:
    for letter in ["A","B","C","D","E","F","G","H","I","J","K","L","M",
                    "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]:
        a.get_url_site(letter)
        a.read_url_site()
        a.get_airport_data(details=True)
    a.create_airport_dataframes()
    # print(" airport_DF ".center(80,'*'))
    # print(a.airport_DF)
    # a.export_dataframe_2_csv(df=a.airport_DF,file_='../data/iata_airport_list.csv')
    # a.export_dataframe_2_csv(df=a.airport_stats_DF,file_='../data/iata_airport_stats_list.csv')
    a.t_end = a.set_end_time()
    a.calculate_runtime(a.t_start, a.t_end)
    
    