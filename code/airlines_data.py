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
        # self.airlines_url_base = "https://en.wikipedia.org/wiki/List_of_airline_codes_(Z)"
        self.airlines_url_base = "https://en.wikipedia.org/wiki/List_of_airline_codes_"

    def create_airlines_df(self,
                           verbose=True):
        self.airlines_DF = pd.DataFrame(columns=['IATA','ICAO','Airline','CallSign','Country','Comments'])
        self.IATA = []
        self.ICAO = []
        self.Airline = []
        self.CallSign = []
        self.Country = []
        self.Comment = []

    def create_url(self,
                   letter='',
                   verbose=True):
        # self.airlines_url = self.airlines_url_base + '({})'.format(letter)
        airlines_url = self.airlines_url_base + '({})'.format(letter)
        return airlines_url

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

    def fill_airlines_df_columns(self,
                                 table=None,
                                 verbose=True):
        for row in table.tbody.find_all('tr'):    
            # Find all data for each column
            columns = row.find_all('td')
            
            if(columns != []):

                # print("....................")
                # print(len(columns))
                iata = columns[0].text.strip()
                # print("iata:",iata)
                # print("type(iata):",type(iata))
                icao = columns[1].text.strip()
                # print(icao)
                airline = columns[2].text.strip()#columns[2].span.contents[0].strip('&0.')
                # print(airline)
                # if airline == 'Akasa Air':
                # print(columns)
                callSign = columns[3].text.strip()#columns[3].span.contents[0].strip('&0.')
                country = columns[4].text.strip()#columns[4].span.contents[0].strip('&0.')
                try:
                    comment = columns[5].text.strip()#columns[5].span.contents[0].strip('&0.')
                except:
                    comment = ''
        
                # self.airlines_DF = self.airlines_DF.append({'IATA': iata,
                #                                             'ICAO': icao,
                #                                             'Airline': airline,
                #                                             'CallSign': callSign,
                #                                             'Country': country,
                #                                             'Comment': comment}, ignore_index=True)
                self.IATA.append(iata)
                self.ICAO.append(icao)
                self.Airline.append(airline)
                self.CallSign.append(callSign)
                self.Country.append(country)
                self.Comment.append(comment)

    def fill_airlines_df(self,
                         verbose=True):
        self.airlines_DF['IATA'] = self.IATA
        self.airlines_DF['ICAO'] = self.ICAO
        self.airlines_DF['Airline'] = self.Airline
        self.airlines_DF['CallSign'] = self.CallSign
        self.airlines_DF['Country'] = self.Country
        self.airlines_DF['Comment'] = self.Comment


    def export_df_2_csv(self,
                        df=None,
                        filename='',
                        verbose=True):
        df.to_csv(filename,index=False)

if __name__ == "__main__":
    print("Airlines")
    a = Airlines()
    a.create_airlines_df()
    # for letter in ['Y','Z']:
    for letter in ["A","B","C","D","E","F","G","H","I","J","K","L","M",
                    "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]:
        airlines_url = a.create_url(letter=letter)
        p = a.read_url(airlines_url)
        soup = a.create_bs_object(page=p)
        table = a.extract_table(soup=soup)
        a.fill_airlines_df_columns(table=table)
    a.fill_airlines_df()
    a.export_df_2_csv(df=a.airlines_DF,
                      filename=r'../data/airlines.csv')
    