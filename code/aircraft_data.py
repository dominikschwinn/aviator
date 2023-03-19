# -*- co+'ding: utf-8 -*-
"""
Created on Sun Mar 19 09:45:55 2023

@author: Dominik Schwinn
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests

class Aircraft():
    def __init__(self):
        print(">>> Aircraft class initialized")
        self.aircraft_url = "https://en.wikipedia.org/wiki/List_of_aircraft_type_designators"

    def create_AC_df(self):
        acDF = pd.DataFrame(columns=['ICAO','IATA','manufacturer','model'])

    def read_url(self,
                 url='',
                 verbose=True):
        p = requests.get(url)
        return p

    def create_bs_object(self,
                         page='',
                         verbose=True):
        soup = bs(page.content, "html.parser")
        return soup

    def extract_table(self,
                      soup='',
                      verbose=True):
        table = soup.find('table', class_='wikitable sortable')
        return table

    def fill_aircraft_df_columns(self,
                                 table=None,
                                 verbose=True):
        for row in table.tbody.find_all('tr'):    
            # Find all data for each column
            columns = row.find_all('td')
            
            if(columns != []):

                print("....................")
                # print(len(columns))
                icao = columns[0].text.strip()
                print(icao)
                iata = columns[1].text.strip()
                print("iata:",iata)
                # print("type(iata):",type(iata))
                model = columns[2].text.strip()#columns[2].span.contents[0].strip('&0.')
                # print(columns)
                print(model)


if __name__ == "__main__":
    a = Aircraft()
    p=a.read_url(a.aircraft_url)
    s = a.create_bs_object(page=p)
    t = a.extract_table(soup=s)
    a.fill_aircraft_df_columns(table=t)