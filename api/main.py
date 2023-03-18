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
##############################################################################################################
#                                functions 
##############################################################################################################
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    for key, value in users.items():
        if credentials.username==key and credentials.password==value:
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
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def calculate_model_performance():
    global feats
    # Chargez le modèle à partir du fichier .pkl
    model = pickle.load(open('../model/rf_regressor.pkl', 'rb'))
    
    # Utilisez les données de test ou de validation pour obtenir les prédictions

    # Vous pouvez utiliser les données de test que vous avez créées précédemment
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

##############################################################################################################
#                                api 
##############################################################################################################

@api.get("/predict")
def predict_close_price(username: str = Depends(get_current_username)):
    # global data
    global feats
    global data
    # data = data.copy()
    

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



@api.get("/price_history/{symbol}/{interval}")
def get_price_history(symbol: str, interval: str, start_time: str, end_time: str, username: str = Depends(get_current_username)):
    # Ici, vous pouvez écrire le code pour récupérer l'historique des prix pour le symbole et l'intervalle donnés
    # Par exemple, interroger la base de données pour obtenir l'historique des prix
    price_history = get_price_history_from_db(symbol, interval, start_time, end_time) # Cette fonction doit être définie par vous

    return {"symbol": symbol, "interval": interval, "price_history": price_history}

@api.post("/add_user")
def add_user(user: dict, username: str = Depends(get_current_username)):
    # Ici, vous pouvez écrire le code pour ajouter un nouvel utilisateur à la base de données
    # Par exemple, insérer les informations de l'utilisateur dans la table des utilisateurs
    user_id = add_user_to_db(user) # Cette fonction doit être définie par vous

    return {"message": "User added successfully", "user_id": user_id}

@api.get("/model_performance")
def get_model_performance(username: str = Depends(get_current_username)):
    performance_metrics = calculate_model_performance() 
    return {"model_performance": performance_metrics}

