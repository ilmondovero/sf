# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 10:39:33 2023

@author: ilmondovero
"""

import pandas as pd

dfs=pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
df=dfs[0]
lista_tickers=df["Symbol"].to_list()
lista_tickers.sort()
