# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 23:18:18 2023

@author: Dominik Schwinn
"""
# import pytest
import os,sys
import pandas as pd
import pickle
import numpy as np
from aviator.src import flight_tracker


class Tests:
    print("Tests")
    def setup_method(self):
        pass

    def test_get_flights():
        pass

    def test_flights_2_df():
        origin = pickle.load(open('./test_files/flights_flightradar.p','rb'))
        # result = 