#%%
import numpy as np
import pandas as pd
from kite_trade import *
import os
# import ta
from tqdm import tqdm
import util_fun as uf
from enctoken import get_kite
kite = get_kite()

# import dask.dataframe as dd

# %%
timerframe_list = [
"day",
"minute",
 "3minute",
 "5minute",
 "10minute",
 "15minute",
 "30minute",
 "60minute",]

i=0
error_list = []
# instument in nse
inst = pd.DataFrame(kite.instruments("NSE"))
inst_filter = inst.query('(name != "")').copy()
inst_filter.rename(columns = {"tradingsymbol":'Symbol'},inplace = True)
# inst_filter.query("Symbol == 'HDFCBANK'")

nifty_500 = pd.read_csv('../data/ind_nifty500list.csv')
nifty_500 = nifty_500.merge(inst_filter, on = 'Symbol')
inst_dict = dict(zip(nifty_500.Symbol, nifty_500.instrument_token))

start_dt = '2018-01-01'
end_dt = '2023-02-27'
time_frame = 'day'
for symbol, instument in tqdm(inst_dict.items()):
    if i :
        print(symbol, instument)
        try:
            df_day = uf.get_data_parllel(kite, instument, time_frame , start_dt,end_dt)
            directory = f'../data/historical/{time_frame}/{symbol}'
            if not os.path.exists(directory):
                os.makedirs(directory)
            df_day.to_parquet(f'{directory}/part0.parquet')
        except:
            print(instument)
            error_list.append(instument)

    i += 1
print(error_list)
    # break
          
# %%
