# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 12:07:49 2023

@author: Dominik Schwinn
"""
import requests
import pandas as pd
import timeit


class Airports(object):
    def __init__(self):
        """
        initializes the Airports class and provides the url-main path

        Returns
        -------
        None.

        """
        self.t_start = self.set_start_time()
        self.url = f"https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:_"
        # self.r = requests.get(url, headers=HEADERS)
        # print(self.r.text)


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


    def get_url_site(self, str_="A"):
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
        self.url = self.url + str_
        print(self.url)


    def read_url_site(self):
        """
        web scraping: reads the url and stores the content in an object
        (type requests.models.Response)

        Returns
        -------
        None.

        """
        HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
        self.r = requests.get(self.url, headers=HEADERS)
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
        if "</a>" in elem[2]:
            airport = elem[2].split("\""">")[1].split("<")[0]
        else:
            airport = elem[2].split("<td>")[1]

        if verbose:
            print("airport name: {}".format(airport))


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
        location = elem[3].split("/td>")[0].split("\""">")[-1].split("<")[0]
        if verbose:
            print("location: {}".format(location))
        return location


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


    def get_airport_data(self):
        """
        extracts the airport data from the Response-object

        Returns
        -------
        None.

        """
        data = self.r.text.split("<tr>")
        #ignoring the first two line since they are not relevant (i.e.filled with data)
        data = data[2:]
        len_data = self.get_data_length(data)

        for i,elem in enumerate(data[2:]):
            print("=============")
            elem = elem.split('</td>')
            iata = self.extract_iata_code(elem)
            icao = self.extract_iata_code(elem)
            airportName = self.extract_airportName(elem)
            location = self.extract_location(elem)
            utc = self.extract_utc((elem))




if __name__ == "__main__":
    a = Airports()
    a.get_url_site("A")
    a.read_url_site()
    a.get_airport_data()
    a.t_end = a.set_end_time()
    a.calculate_runtime(a.t_start, a.t_end)
    