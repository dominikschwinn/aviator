# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 12:07:49 2023

@author: Dominik Schwinn
"""
import requests
# import pandas as pd


class Airports(object):
    def __init__(self):
        """
        initializes the Airports class and provides the url-main path

        Returns
        -------
        None.

        """

        self.url = f"https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:_"
        # self.r = requests.get(url, headers=HEADERS)
        # print(self.r.text)

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

    def extract_iata_code(self,elem):
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
        print("iata: ",iata)
        return iata

    def extract_icao_code(self,elem):
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
        print("icao:",icao)   
        return icao

    def extract_airportName(self,elem):
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

        print("airport name:", airport)

    def extract_location(self,elem):
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
        print("location:",location)
        return location


    def get_airport_data(self):
        """
        extracts the airport data from the Response-object

        Returns
        -------
        None.

        """
        data = self.r.text.split("<tr>")
        for i,elem in enumerate(data[2:]):
            print("=============")
            elem = elem.split('</td>')
            iata = self.extract_iata_code(elem)
            icao = self.extract_iata_code(elem)
            airportName = self.extract_airportName(elem)
            location = self.extract_location(elem)


if __name__ == "__main__":
    a = Airports()
    a.get_url_site("A")
    a.read_url_site()
    a.get_airport_data()
    