import csv

from binance.client import Client
from binance import ThreadedWebsocketManager
from binance.enums import *


import json
from datetime import datetime
import time
import pandas as pd
from Crendentials import api_key, api_secret
client = Client(api_key, api_secret)

def getData(coin : str , bar :int , nu_unit_lookback : int, unit_lookback: str ):
    """
        Récupère les données historiques de la paire de trading donnée à partir de l'API de Binance.

        Args:
            coin (str): La paire de trading à récupérer (par exemple, 'BTC').
            bar (int): L'intervalle de temps entre chaque bougie en minutes. C'est le timeframe (3, 15, 30)
            nu_unit_lookback (int): Le nombre d'unités de lookback à récupérer. (combien de bougie on veut récuperer)
            unit_lookback (str): L'unité de temps pour le lookback (par exemple, 'day' pour jour, 'hour' pour heure, 'minute' pour minute).

        Returns:
            pandas.DataFrame: Un DataFrame contenant les données historiques de la paire de trading.
        """
    symbol, interval, lookback = (
        coin + "USDT",
        str(bar) + "m",
        str(nu_unit_lookback) + " " + unit_lookback
    )
    try:
        df = pd.DataFrame(
            client.get_historical_klines(symbol, interval, lookback + " ago UTC")
        )
    except:
        df = pd.DataFrame(
            columns=[
                "Time",
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
                "CloseTime",
                "QuoteAssetVolume",
                "NumberOfTrades",
            ]
        )
    if df.empty:
        return df
    df = df.iloc[:, :9]
    df.columns = [
        "Time",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "CloseTime",
        "QuoteAssetVolume",
        "NumberOfTrades",
    ]
    df.CloseTime = pd.to_datetime(df.CloseTime.values, unit="ms")
    df = df.astype({"Close": "float"})
    df = df.astype({"Open": "float"})
    df = df.astype({"High": "float"})
    df = df.astype({"Low": "float"})
    df = df.astype({"Volume": "float"})
    df = df.astype({"QuoteAssetVolume": "float"})
    return df
##FOR TEST
#print(getData('BTC',15, 24, 'h'))
#print(client.KLINE_INTERVAL_1DAY)



def start_streaming_data(symbol: str, interval: str, output_type: str) -> None:
    num_msgs = 0
    start_time = time.time()
    print("11111111111111111111111")

    def callback_fct(data):
        print("Received new klines:")
        print(data)
        json_data = json.loads(data)
        kline = json_data['k']
        candle_data = [
            datetime.fromtimestamp(kline['t'] / 1000),
            float(kline['o']),
            float(kline['h']),
            float(kline['l']),
            float(kline['c']),
            float(kline['v']),
            datetime.fromtimestamp(kline['T'] / 1000),
            float(kline['q']),
            int(kline['n'])
        ]
        if output_type == 'json':
            with open(f'{symbol}_{interval}.json', 'w', newline='') as jsonfile:
                writer = json.writer(jsonfile)
                writer.writerow(candle_data)
        elif output_type == 'csv':
            with open(f'{symbol}_{interval}.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(candle_data)

    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    twm.start()
    print("222222222222222222")

    twm.start_kline_socket(callback=callback_fct, symbol=symbol, interval=KLINE_INTERVAL_1MINUTE)
    print("333333333333333333333333")


    print("44444444444444444444444444")

start_streaming_data('BTCUSDT', '1m','csv')



