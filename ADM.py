# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 10:03:30 2018
@author: Dario Marinelli

"""
from tiingo import TiingoClient #pip install tiingo se manca il pacchetto su anaconda
import pandas as pd
capital=100000
config = {}
config['session'] = True
config['api_key'] = "set yours https://api.tiingo.com/account/api/token"
client = TiingoClient(config)
capitale=100000#capitale iniziale
spy=client.get_dataframe("SPY",frequency='monthly',metric_name='adjClose',startDate='2007-01-01')#scarico sp500
scz=client.get_dataframe("SCZ",frequency='monthly',metric_name='adjClose',startDate='2007-01-01')#scarico scz
tlt=client.get_dataframe("TLT",frequency='monthly',metric_name='adjClose',startDate='2007-01-01')#scarico tlt
df=pd.concat([spy,scz,tlt], axis=1).dropna()#allineo gli storici ed elimino i buchi nei dati
df.columns=["SPY","SCZ","IEF"]#rinomino le colonne
df_az=df[["SPY","SCZ"]].copy()#copio i dati azionari in un dataframe
df_ob=df["IEF"].copy()#copio i dati obbligazionari in un dataframe
df_az_momentum=(df_az.pct_change()+df_az.pct_change(3)+df_az.pct_change(6)).shift().dropna()#calcolo il momentum a 1,3,6 mesi
df_az_rank=df_az_momentum.rank(axis=1,ascending=False).applymap(lambda x:0 if x>1 else 1)#faccio la classifica per vedere il più forte
df_azionario=(df_az_momentum>0).sum(axis=1).apply(lambda x:1 if x>=1 else 0)#applico il segnale all'azionario
df_obbligazionario=df_azionario.apply(lambda x:1 if x==0 else 0)#applico il segnale opposto all'obbligazionario
df_rendimento_az=((df_az_rank*df_az.pct_change()).sum(axis=1)*df_azionario)
df_rendimento_ob=(df_ob.pct_change()*df_obbligazionario).dropna()#sommo i rendimenti tra azionario e obbligazionario
df_az["ADM"]=((1+(df_rendimento_az+df_rendimento_ob)).cumprod()-1)*capitale+capitale#faccio la produttoria dei rendimenti sui soldi
df_az["AZ"]=((1+(df_rendimento_az)).cumprod()-1)*capitale+capitale
df_az["OBB"]=((1+(df_rendimento_ob)).cumprod()-1)*capitale+capitale
df_az["TLT"]=((1+(df_ob.pct_change())).cumprod()-1)*capitale+capitale
df_az.dropna(inplace=True)#cancello i dati mancanti
df_az=(df_az/df_az.iloc[0])*100#normalizzo a 100
df_az.plot(use_index=True,legend=True,title="Accelerating Dual Momentum")#Plotto la Equity