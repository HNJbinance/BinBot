import pandas as pd
import requests
import json 

# Récupération des données à partir de l'API Binance
response = requests.get('https://api.binance.com/api/v3/klines',
                                      params={'symbol': 'BTCUSDT',
                                                'interval': '1d'})
data = response.json()

# Conversion des données en DataFrame pandas
df = pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 
                                        'Volume', 'Close time', 
                                        'Quote asset volume', 'Number of trades', 
                                        'Taker buy base asset volume', 
                                        'Taker buy quote asset volume', 'Ignore'])

# Conversion des timestamps en date
df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')

# Renommer les colonnes pour une meilleure compréhension
df.rename(columns={'Open': 'open_price', 'Close': 'close_price', 'Volume': 'volume'},
                        inplace=True)

# Supprimer les colonnes inutiles
df.drop(columns=['High', 'Low', 'Quote asset volume', 'Number of trades',
                            'Taker buy base asset volume', 
                            'Taker buy quote asset volume', 'Ignore'], inplace=True)

# Mettre en index la colonne 'Open time'
df.set_index('Open time', inplace=True)

# Sauvegarder les données nettoyées dans un nouveau fichier CSV
df.to_json('binance_data.json', orient='records')

#df.to_csv('binance_data.csv', index=True)
