# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 08:24:45 2023

@author: ilmondovero 
"""

from tiingo import TiingoClient
import pandas as pd
config = {}
config['session'] = True
config['api_key'] = "fbb82277db40c7a1924d0a5bcf1d563bd21323cd"
client = TiingoClient(config)
capitale = 100000
df=client.get_dataframe(["GLD","IWN","SHY","SPY","TLT"],startDate="1980-01-01",metric_name="adjClose").dropna()
rendimenti=df.pct_change().dropna()
portafoglio=0.2*rendimenti["GLD"]+0.2*rendimenti["IWN"]+0.2*rendimenti["SHY"]+0.2*rendimenti["SPY"]+0.2*rendimenti["TLT"]
equity=(1+portafoglio).cumprod()*capitale
equity.plot()