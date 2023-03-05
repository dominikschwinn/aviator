# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 10:12:58 2023

@author: Dominik Schwinn
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests

class Airlines():
    def __init__(self):
        print(">>> initializing Airlines class")

        # airlines_url = "https://en.wikipedia.org/wiki/List_of_airline_codes"
        self.airlines_url = "https://en.wikipedia.org/wiki/List_of_airline_codes_(Z)"

    def create_airlines_df(self,
                           verbose=True):
        self.airlines_DF = pd.DataFrame(columns=['IATA','ICAO','Airline','CallSign','Country','Comments'])

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

    # print('Classes of each table:')
    # for table in soup.find_all('table'):
    #     print(table.get('class'))

    def fill_airlines_df(self,
                         table=None,
                         verbose=True):
        for row in table.tbody.find_all('tr'):    
            # Find all data for each column
            columns = row.find_all('td')
            
            if(columns != []):
                iata = columns[0].text.strip()
                icao = columns[1].text.strip()
                airline = columns[2].text.strip()#columns[2].span.contents[0].strip('&0.')
                callSign = columns[3].text.strip()#columns[3].span.contents[0].strip('&0.')
                country = columns[4].text.strip()#columns[4].span.contents[0].strip('&0.')
                comment = columns[5].text.strip()#columns[5].span.contents[0].strip('&0.')
        
                self.airlines_DF = self.airlines_DF.append({'IATA': iata,
                                                            'ICAO': icao,
                                                            'Airline': airline,
                                                            'CallSign': callSign,
                                                            'Country': country,
                                                            'Comment': comment}, ignore_index=True)    

if __name__ == "__main__":
    print("Airlines")
    a = Airlines()
    a.create_airlines_df()
    p = a.read_url(a.airlines_url)
    soup = a.create_bs_object(page=p)
    table = a.extract_table(soup=soup)
    a.fill_airlines_df(table=table)
    