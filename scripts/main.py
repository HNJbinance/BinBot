import pickle
import modules.sql_properties as sql
import pandas as pd
import numpy as np
from fastapi import FastAPI

from datetime import datetime

#############################################################################################
#                                          init
#############################################################################################
app = FastAPI()
sql = sql.SqlAction()

#############################################################################################
#                                          data
#############################################################################################



#############################################################################################
#                                          functions
#############################################################################################

def decision(actual_close_price: float, predict_close_price: float):
    if actual_close_price > predict_close_price:
        return "sell"
    elif actual_close_price < predict_close_price:
        return "buy"
    else:
        return "hold"
#############################################################################################
#                                          endpoint
#############################################################################################

@app.get("/predict")
def predict_close_price():
    """
    Prédit le prix de clôture pour la prochaine heure en utilisant le modèle entraîné RandomForestRegressor.

    Retourne:
        Un dictionnaire contenant les informations suivantes:
        - symbol (str): Le symbole de la paire de trading, par exemple "BTC/USDT".
        - interval (str): L'intervalle de temps pour la prédiction, ici "1h" pour une heure.
        - actual_time (str): L'heure actuelle au format 'YYYY-MM-DD HH:MM:SS'.
        - actual_price (float): Le prix de clôture actuel récupéré depuis le flux en temps réel.
        - next_hour (str): L'heure de la prochaine prédiction au format 'YYYY-MM-DD HH:MM:SS'.
        - predicted_close_price (float): Le prix de clôture prédit pour la prochaine heure, arrondi à 2 décimales.
        - decision (str): La décision recommandée basée sur la prédiction ("buy", "sell" ou "hold").
    """
    close_price_stream = sql.retrieve_stream_price_and_next_hour()[0]["close_price"]
    next_hour = sql.retrieve_stream_price_and_next_hour()[0]["next_hour"]
    feats, _ = sql.retrieve_historical_klines_dataframe()
    next_hour_data = feats.iloc[-1:]
    model = pickle.load(open("../models/model_opt_rfc.pkl", "rb"))

    # Predict the close price for the next hour
    next_hour_data = feats.iloc[-1:]
    next_hour_close_price = model.predict(next_hour_data)
    actual_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "symbol": "BTC/USDT",
        "interval": "1h",
        "actual_time": actual_time,
        "actual_price": close_price_stream,
        "next_hour": next_hour,
        "predicted_close_price": round(next_hour_close_price.item(), 2),
        "decision": decision(close_price_stream, next_hour_close_price),
    }
