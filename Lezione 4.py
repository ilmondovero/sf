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
strategy = {
    "All Weather": {"DBC": 7.5, "GLD": 7.5, "IEF": 15, "SPY": 30, "TLT": 40},
    "Benchmark 60/40": {"SPY": 60, "IEF": 40},
    "Golden Butterfly": {"GLD": 20, "IWN": 20, "SHY": 20, "SPY": 20, "TLT": 20},
}
ticker = set().union(*(d.keys() for d in strategy.values()))
df=client.get_dataframe(ticker,startDate="1980-01-01",metric_name="adjClose").dropna()
rendimenti=df.pct_change().dropna()
portafoglio_GB=rendimenti[["DBC", "GLD", "IEF", "SPY", "TLT"]].sum(axis=1)/5
equity_GB=(1+portafoglio_GB).cumprod()*capitale
portafoglio_BK=0.6*rendimenti["SPY"]+0.4*rendimenti["IEF"]
equity_BK=(1+portafoglio_BK).cumprod()*capitale
portafoglio_AW=0.075*rendimenti["DBC"]+0.075*rendimenti["GLD"]+0.15*rendimenti["IEF"]+0.3*rendimenti["SPY"]+0.4*rendimenti["TLT"]
equity_AW=(1+portafoglio_AW).cumprod()*capitale
equity=pd.concat([equity_GB,equity_BK,equity_AW],axis=1)
equity.columns=["Golden Butterfly","Benchmark 60/40","All Weather"]
equity2=equity/equity.iloc[0]*100
equity2.plot()