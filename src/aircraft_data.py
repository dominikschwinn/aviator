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
        
        self.ICAO = []
        self.IATA = []
        self.MANUFACTURER = []
        self.MODEL = []
        
        self.manufacturers_list = ['Airbus','Antonov','Aerospatiale','Avro',
                                   'Boeing','Bombardier','Bell','Beechcraft','British Aerospace',
                                   'Canadair', 'Cessna','Cirrus',
                                   'Dassault','De Havilland','Daher',
                                   'Embraer','Eurocopter',
                                   'Fairchild','Fokker',
                                   'Gulfstream','Grumman',
                                   'Honda','Hawker Siddeley','Hawker',
                                   'Ilyushin','Israel Aircraft Industries',
                                   'Junkers',
                                   'Lockheed','Learjet',
                                   'McDonnell Douglas','MIL',  'Mitsubishi',
                                   'Piaggio','Piper','Pilatus','Partenavia',
                                   'Sikorsky','Saab','Sukhoi','Shorts',
                                   'Tupolev','Tecnam', 
                                   'Yakovlev',
                                   ]
        self.create_AC_df()

    def create_AC_df(self):
        """
        creates the dataframe self.acDF with the columns:
        'ICAO','IATA','manufacturer','model'

        Returns
        -------
        None.

        """
        self.acDF = pd.DataFrame(columns=['ICAO','IATA','manufacturer','model'])

    def read_url(self,
                 url='',
                 verbose=True):
        """
        

        Parameters
        ----------
        url : TYPE, optional
            DESCRIPTION. The default is ''.
        verbose : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        p : TYPE
            DESCRIPTION.

        """
        p = requests.get(url)
        return p

    def create_bs_object(self,
                         page='',
                         verbose=True):
        """
        

        Parameters
        ----------
        page : TYPE, optional
            DESCRIPTION. The default is ''.
        verbose : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        soup : TYPE
            DESCRIPTION.

        """
        soup = bs(page.content, "html.parser")
        return soup

    def extract_table(self,
                      soup='',
                      verbose=True):
        """
        

        Parameters
        ----------
        soup : TYPE, optional
            DESCRIPTION. The default is ''.
        verbose : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        table : TYPE
            DESCRIPTION.

        """
        table = soup.find('table', class_='wikitable sortable')
        return table

    def get_manufacturer_from_model(self,
                                    model=None,
                                    verbose=False):
        """
        

        Parameters
        ----------
        model : TYPE, optional
            DESCRIPTION. The default is None.
        verbose : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE
            DESCRIPTION.
        model : TYPE
            DESCRIPTION.

        """
        manufacturer = ''
        for elem in self.manufacturers_list:
            if elem in model:
                manufacturer = elem
                # model = model.split('{} '.format(manufacturer))[1]
                break
        return manufacturer#, model

    def revise_model(self,
                     model=None,
                     manufacturer=None,
                     verbose=False):
        try:
            model = model.split('{} '.format(manufacturer))[1]
        except:
            pass
        return model
        

    def fill_aircraft_df_columns(self,
                                 table=None,
                                 verbose=True):
        for row in table.tbody.find_all('tr'):    
            # Find all data for each column
            columns = row.find_all('td')
            
            if(columns != []):

                # print("....................")
                icao = columns[0].text.strip()
                # print(icao)
                iata = columns[1].text.strip()
                # print("iata:",iata)
                model = columns[2].text.strip()#columns[2].span.contents[0].strip('&0.')
                # print(model)
                # manufacturer, model = self.get_manufacturer_from_model(model=model)
                manufacturer = self.get_manufacturer_from_model(model=model)
                model = self.revise_model(model=model,
                                          manufacturer=manufacturer)
                
                self.ICAO.append(icao)
                self.IATA.append(iata)
                self.MODEL.append(model)
                self.MANUFACTURER.append(manufacturer)


    def fill_aircraft_df(self,
                         verbose=False):
        self.acDF['ICAO'] = self.ICAO#
        self.acDF['IATA'] = self.IATA
        self.acDF['manufacturer'] = self.MANUFACTURER
        self.acDF['model'] = self.MODEL

    def export_df_2_csv(self,
                        df=None,
                        filename='',
                        verbose=False):
        df.to_csv(filename, index=False)


if __name__ == "__main__":
    a = Aircraft()
    p=a.read_url(a.aircraft_url)
    s = a.create_bs_object(page=p)
    t = a.extract_table(soup=s)
    a.fill_aircraft_df_columns(table=t)
    a.fill_aircraft_df()
    a.export_df_2_csv(df=a.acDF,
                      filename=r'../data/aircraft.csv')