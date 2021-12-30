from binance.client import Client
import pandas as pd
from datetime import datetime, timedelta


BINANCE = {
  "key": "",
  "secret": ""
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

    candles = client.get_historical_klines(symbol=exchange, interval='30m', start_str=str(datetime.now() - timedelta(days=365)) )
    df = parser(candles)
    df.to_csv('./DATA/{}.csv'.format(exchange),index=False)

if __name__ == '__main__':

    for i in ['BTCUSDT','ETHUSDT']:
        last_data(i)
