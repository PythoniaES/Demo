from binance.client import Client
import pandas as pd
from datetime import datetime, timedelta
import os

BINANCE = {
  "key": "3twyIVmgSoinkU39hx2Mubt8bREk3O2k2lSfw29LNDfw7u57twEUNQLbvQiJBTVu",
  "secret": "AY01aIZp5yB77sfXnqx34xDvz9xdq0HvZK6evRFze8QWAEdYG5uyDRPsjocUW3Mv"
}


client = Client(BINANCE['key'], BINANCE['secret'])

def parser(data):
    df = pd.DataFrame(data)
    df = df.drop([6, 7, 8, 9, 10, 11], axis=1)

    col_names = ['time', 'open', 'high', 'low', 'close', 'volume']
    df.columns = col_names
    for col in col_names:
        df[col] = df[col].astype(float)
    df['start'] = pd.to_datetime(df['time'] * 1000000)

    return df

def last_data(exchange):
    if not os.path.exists('./DATA'):
        os.mkdir('./DATA')
    candles = client.get_historical_klines(symbol=exchange, interval='30m', start_str=str(datetime.now() - timedelta(days=365)) )
    df = parser(candles)
    df.to_csv('./DATA/{}.csv'.format(exchange),index=False)

if __name__ == '__main__':

    for i in ['BTCEUR','ADAEUR','ETHEUR','LUNAEUR','AVAXEUR','SOLEUR','XRPEUR','DOTEUR','DOGEEUR']:
        last_data(i)
