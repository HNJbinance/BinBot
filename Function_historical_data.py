from binance.client import Client, AsyncClient
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

data = getData('BTC',15, 24, 'h')
data.to_csv('historical_data.csv', index=False)