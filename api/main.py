# import mysql.connector

from datetime import timedelta, datetime

import pandas as pd
from fastapi import FastAPI
from sklearn.ensemble import RandomForestRegressor
import pickle
import warnings
warnings.filterwarnings('ignore')
from pydantic import BaseModel


from fastapi import Depends,  HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

df = pd.read_csv("../model/data.csv")
model = pickle.load(open('../model/rf_regressor.pkl','rb'))

api = FastAPI()

security = HTTPBasic()

# cnx = mysql.connector.connect(user='root', password='temp123',
#                               host='172.17.0.2', port='3306',
#                               database='opa')
# ## remplacer host par l'ID de votre machine virtuelle 
# ## port : représente le port ou elle est logée notre DB sur le docker 
# cursor = cnx.cursor()



## Authentifiaction & authorisation :
users = {
  "ilham": "noumir",
  "hamza": "ennaji",
  "loic": "montagnac",
   "souhila" : "lebib",
    "simon" : "cariou"
}

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    for key, value in users.items():
        if credentials.username==key and credentials.password==value:
            return credentials.username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


@api.get("/predict")
def predict_close_price(username: str = Depends(get_current_username)):
    data = df.copy()

    data['close_time'] = pd.to_datetime(data['close_time'], unit='ms')
    data = data.set_index('close_time')
    data.sort_index(inplace=True)

    # Fill any missing values
    data = data.ffill()

    # Create lagged features for the Random Forest model
    lag_columns = ['open_price', 'high_price', 'low_price', 'close_price', 'volume', 
               'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 
               'taker_buy_quote_asset_volume']

    lag_count = 6

    for col in lag_columns:
        for lag in range(1, lag_count + 1):
            data[f'{col}_lag{lag}'] = data[col].shift(lag)

    # Supprimer les lignes avec des valeurs manquantes après la création des colonnes décalées
    data.dropna(inplace=True)

    # Split the data into training and testing sets
    feats = data.drop(['close_price', 'id_symint', 'open_time'], axis=1)
    target = data['close_price']

    # Predict the close price for the next hour
    next_hour = data.index[-1] + timedelta(hours=1)
    next_hour_data = feats.iloc[-1:]
    next_hour_close_price = model.predict(next_hour_data)[0]
    actual_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {"symbol":"BTC/USDT", "interval": "1h", "actual_time":actual_time,  "actual_price":"streaming", "next_hour": next_hour.strftime("%Y-%m-%d %H:%M:%S"), "predicted_close_price": round(next_hour_close_price, 2),  "decision":"#######"}
    #return {"predicted_close_price": round(next_hour_close_price, 2)}



