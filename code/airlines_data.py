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

    def read_url(self,
                 url='',
                 verbose=True):
        p = requests.get(url)
        return p

    def create_BS_object(self,
                         page='',
                         verbose=True):
        soup = bs(page.content, "html.parser")
        return soup




if __name__ == "__main__":
    print("Airlines")
    a = Airlines()