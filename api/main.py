import mysql.connector

from datetime import timedelta, datetime

import pandas as pd
from fastapi import FastAPI
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import pickle
import warnings
warnings.filterwarnings('ignore')
from pydantic import BaseModel


from fastapi import Depends,  HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


##############################################################################################################
#                                Initialisation : connection, cursor, dataframe
##############################################################################################################
api = FastAPI()
security = HTTPBasic()
cnx = mysql.connector.connect(user='root', password='temp123',
                              host='172.17.0.2', port='3306',
                              database='opa')
cursor = cnx.cursor()

# df = pd.read_csv("../model/data.csv")
model = pickle.load(open('../model/rf_regressor.pkl','rb'))
##############################################################################################################
#                                Constantes
##############################################################################################################
# Authentifiaction & authorisation :
users = {
  "ilham": "noumir",
  "hamza": "ennaji",
  "loic": "montagnac",
   "souhila" : "lebib",
    "simon" : "cariou"
}
lag_columns = ['open_price', 'high_price', 'low_price', 'close_price', 'volume', 
               'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 
               'taker_buy_quote_asset_volume']

lag_count = 6
##############################################################################################################
#                                prepare data for prediction and performance test
##############################################################################################################
query1 = "SELECT * FROM historical_klines"
cursor.execute(query1)
# Load the data into a Pandas DataFrame
data = pd.DataFrame(cursor.fetchall(), columns=['id_symint', 'open_time', 'open_price', 'high_price', 'low_price',
       'close_price', 'volume', 'close_time', 'quote_asset_volume',
       'number_of_trades', 'taker_buy_base_asset_volume',
       'taker_buy_quote_asset_volume'])


data['close_time'] = pd.to_datetime(data['close_time'], unit='ms')
data = data.set_index('close_time')
data.sort_index(inplace=True)

# Fill any missing values
data = data.ffill()    
# Create lagged features for the Random Forest model
for col in lag_columns:
    for lag in range(1, lag_count + 1):
        data[f'{col}_lag{lag}'] = data[col].shift(lag)

# Supprimer les lignes avec des valeurs manquantes après la création des colonnes décalées
data.dropna(inplace=True)

# Split the data into training and testing sets
feats = data.drop(['close_price', 'id_symint', 'open_time'], axis=1)
target = data['close_price']

query2 = "SELECT close_price FROM stream_klines"
cursor.execute(query2)
result = cursor.fetchall()
close_price_stream_list = [row[0] for row in result]
close_price_stream = close_price_stream_list[0]

# Prepare a SELECT query to check the username and password against the api_users table
query3 = "SELECT login, password FROM api_users WHERE is_active = 1"
cursor.execute(query3)
rows = cursor.fetchall()




##############################################################################################################
#                                functions 
##############################################################################################################
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    for user in rows:
        if credentials.username==user[0] and credentials.password==user[1]:
            return credentials.username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
def decision(actual_close_price: float, predict_close_price: float):
    if actual_close_price > predict_close_price:
        return "sell"
    elif actual_close_price < predict_close_price:
        return "buy"
    else:
        return "hold"

def add_user_to_db(user):
    pass 

def calculate_model_performance():
    global feats
    model = pickle.load(open('../model/rf_regressor.pkl', 'rb'))
    y_pred = model.predict(feats)
    # Calculez les métriques de performance
    mae = mean_absolute_error(target, y_pred)
    mse = mean_squared_error(target, y_pred)
    rmse = mean_squared_error(target, y_pred, squared=False)
    r2 = r2_score(target, y_pred)
    
    performance_metrics = {
        "mean_absolute_error": mae,
        "mean_squared_error": mse,
        "root_mean_squared_error": rmse,
        "r2_score": r2
    }
    return performance_metrics

def get_price_history_from_db(start_time: str, end_time: str, interval: str, symbole:str ='BTC'):
    global data
    df_price= data[['close_price']]
    df_price.index = pd.to_datetime(df_price.index)
    filtered_data = df_price[start_time:end_time]
    resampled_data = filtered_data.resample(interval).last()
    price_history = resampled_data.to_dict()
    prices_data = []
    for date, price in price_history['close_price'].items():
        prices_data.append({"symbol":"BTC","interval":interval,"date": date.strftime('%Y-%m-%d %H:%M:%S'), "price": price})
    
    return prices_data

def calculate_moving_average(data: pd.DataFrame, window: int):
    return data['close_price'].rolling(window=window).mean()

##############################################################################################################
#                                api 
##############################################################################################################

@api.get("/predict")
def predict_close_price(username: str = Depends(get_current_username)):
    """
    Prédit le prix de clôture pour la prochaine heure en utilisant le modèle entraîné RandomForestRegressor.
    
    L'utilisateur doit être authentifié pour accéder à cette fonction.
    
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
    # global data
    global feats
    global data    
    # Predict the close price for the next hour
    next_hour = data.index[-1] + timedelta(hours=1)
    next_hour_data = feats.iloc[-1:]
    next_hour_close_price = model.predict(next_hour_data)[0]
    actual_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"symbol":"BTC/USDT", 
            "interval": "1h", 
            "actual_time":actual_time,  
            "actual_price":close_price_stream, 
            "next_hour": next_hour.strftime("%Y-%m-%d %H:%M:%S"), 
            "predicted_close_price": round(next_hour_close_price, 2),  
            "decision":decision(close_price_stream, next_hour_close_price)}

@api.get("/price_history/{start_time}/{end_time}/{interval}/{symbol}")
def get_price_history(start_time: str, end_time: str, interval: str, symbol:str ='BTC', username: str = Depends(get_current_username)):
    """
    Récupère l'historique des prix d'une crypto-monnaie entre deux dates spécifiées, avec une fréquence définie.
    Args:
        start_time (str): Date de début sous forme de chaîne de caractères au format 'YYYY-MM-DD'.
        end_time (str): Date de fin sous forme de chaîne de caractères au format 'YYYY-MM-DD'.
        interval (str): Fréquence de l'échantillonnage. '1H' pour une heure, '7D' pour une semaine, '1M' pour un mois .
        symbole (str): Symbole de la crypto-monnaie (par défaut 'BTC').
    
    Exemple:
        Pour récupérer l'historique des prix du Bitcoin (BTC) entre  :  '2023-02-17 16:59:59' ET '2023-03-17 20:59:59'
        
        >>> Sur Postamn :http://127.0.0.1:8000/price_history/2023-02-16 16:59:59/2023-03-16 20:59:59/7D/BTC
    """
    price_history = get_price_history_from_db(start_time, end_time, interval, symbol)
    return price_history

@api.post("/add_user")
def add_user(user: dict, username: str = Depends(get_current_username)):
    user_id = add_user_to_db(user) 
    return {"message": "User added successfully", 
            "user_id": user_id}

@api.get("/model_performance")
def get_model_performance(username: str = Depends(get_current_username)):
    """
    Calcule et retourne les métriques de performance du modèle RandomForestRegressor pour les données d'entraînement.
    
    L'utilisateur doit être authentifié pour accéder à cette fonction.
    
    Retourne:
        Un dictionnaire contenant les métriques de performance suivantes :
        - mean_absolute_error (float): L'erreur absolue moyenne entre les prédictions du modèle et les valeurs réelles.
        - mean_squared_error (float): L'erreur quadratique moyenne entre les prédictions du modèle et les valeurs réelles.
        - root_mean_squared_error (float): La racine carrée de l'erreur quadratique moyenne.
        - r2_score (float): Le coefficient de détermination R², qui mesure la proportion de la variance expliquée par le modèle.
    """
    performance_metrics = calculate_model_performance() 
    return {"model_performance": performance_metrics}

@api.get("/moving_averages/{symbol}/{interval}/{window}")
def get_moving_averages(symbol: str, interval: str, window: int, username: str = Depends(get_current_username)):
    """
    Calcule et renvoie les moyennes mobiles pour un symbole de trading, un intervalle de temps et une fenêtre de temps spécifiés.
    
    Args:
        symbol (str): Le symbole de la paire de trading, par exemple "BTC/USDT".
        interval (str): L'intervalle de temps pour le calcul, par exemple "1h" pour une heure.
        window (int): La taille de la fenêtre pour le calcul de la moyenne mobile.
    
    L'utilisateur doit être authentifié pour accéder à cette fonction.
    
    Retourne:
        Un dictionnaire contenant les informations suivantes:
        - symbol (str): Le symbole de la paire de trading, par exemple "BTC/USDT".
        - interval (str): L'intervalle de temps pour le calcul, par exemple "1h" pour une heure.
        - moving_average (pd.Series): La série temporelle des moyennes mobiles calculées.
    """
    global data

    resampled_data = data[['close_price']].resample(interval).last()
    moving_averages = calculate_moving_average(resampled_data, window)
    
    moving_averages_data = []
    for date, value in moving_averages.items():
        moving_averages_data.append({"symbol": symbol, "interval": interval, "date": date.strftime('%Y-%m-%d %H:%M:%S'), "moving_average": value})
    
    return moving_averages_data
