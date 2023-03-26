import mysql.connector

from datetime import timedelta, datetime

import pandas as pd
from fastapi import FastAPI
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import pickle
import warnings
import os
warnings.filterwarnings("ignore")
from pydantic import BaseModel


from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

##############################################################################################################
#                                Initialisation : connection, cursor, dataframe
##############################################################################################################
api = FastAPI()
security = HTTPBasic()
cnx = mysql.connector.connect(
    user="root", password=os.environ.get("MYSQL_PASSWORD"), host=os.environ.get('MYSQL_ADDRESS'), port="3306", database="opa"
)
cursor = cnx.cursor()
# df = pd.read_csv("../model/data.csv")
model = pickle.load(open("/trainapi/model/best_model.pkl", "rb"))

##############################################################################################################
#                                Constantes
##############################################################################################################
lag_columns = [
    "open_price",
    "high_price",
    "low_price",
    "close_price",
    "volume",
    "quote_asset_volume",
    "number_of_trades",
    "taker_buy_base_asset_volume",
    "taker_buy_quote_asset_volume",
]

lag_count = 6


##############################################################################################################
#                                functions for data handling
##############################################################################################################
def retrieve_hklines_db():
    query1 = "SELECT * FROM historical_klines"
    cursor.execute(query1)
    # Load the data into a Pandas DataFrame
    df = pd.DataFrame(
        cursor.fetchall(),
        columns=[
            "id_symint",
            "open_time",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
        ],
    )
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    df = df.set_index("close_time")
    df.sort_index(inplace=True)
    # Fill any missing values
    df = df.ffill()
    return df


data = retrieve_hklines_db()


def create_lag_column(df):
    # Create lagged features for the Random Forest model
    for col in lag_columns:
        for lag in range(1, lag_count + 1):
            df[f"{col}_lag{lag}"] = df[col].shift(lag)
    df["next_close_price"] = df["close_price"].shift(-1)
    # Supprimer les lignes avec des valeurs manquantes après la création des colonnes décalées
    df.dropna(inplace=True)
    return df


data = create_lag_column(data)


# Split the data into training and testing sets
def split_data_features_target(df):
    feats = df.drop(["close_price", "id_symint", "open_time"], axis=1)
    target = df["next_close_price"]
    return feats, target


feats, target = split_data_features_target(data)


def retrieve_sklines_db() -> float:
    query2 = "SELECT close_price FROM stream_klines"
    cursor.execute(query2)
    result = cursor.fetchall()
    close_price_stream_list = [row[0] for row in result]
    close_price_stream = close_price_stream_list[0]
    return close_price_stream


close_price_stream = retrieve_sklines_db()


# Prepare a SELECT query to check the username and password against the api_users table
def retrieve_active_users() -> list:
    query3 = "SELECT login, password FROM api_users WHERE is_active = 1"
    cursor.execute(query3)
    rows = cursor.fetchall()
    return rows


rows = retrieve_active_users()


##############################################################################################################
#                                functions
##############################################################################################################
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    for user in rows:
        if credentials.username == user[0] and credentials.password == user[1]:
            return credentials.username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def add_user_to_db(
    id_api_users: int, name: str, lastname: str, login: str, password: str
):
    # Prepare an INSERT query to add the new user to the api_users table
    query = "INSERT INTO api_users (id_api_users , name, lastname, date_insert , date_update , last_login , is_active, login, password, validity_day ) VALUES (%s, %s, %s,NOW(),NOW(),NULL,TRUE,%s,%s,180)"
    values = (id_api_users, name, lastname, login, password)
    # Execute the query and commit the transaction
    cursor.execute(query, values)
    cnx.commit()
    # Close the database connection
    cnx.close()
    # Print a message indicating that the user has been created
    print("User created successfully")


def update_user_db(
    id_api_users: int, name: str, lastname: str, login: str, password: str
):
    # Prepare an UPDATE query to modify the existing user in the api_users table
    query = "UPDATE api_users SET name = %s, lastname = %s, login = %s, password = %s WHERE id_api_users = %s"
    values = (name, lastname, login, password, id_api_users)

    # Execute the query and commit the transaction
    cursor.execute(query, values)
    cnx.commit()

    # Close the database connection
    cnx.close()

    # Return a JSON response indicating that the user has been updated
    return {"message": "User updated successfully"}


def delete_user_db(id_api_users: int):
    # Prepare a DELETE query to remove the existing user from the api_users table
    query = "DELETE FROM api_users WHERE id_api_users = %s"
    values = (id_api_users)

    cursor.execute(query, values)
    cnx.commit()

    # Close the database connection
    cnx.close()

    # Return a JSON response indicating that the user has been deleted
    return {"message": "User deleted successfully"}


def decision(actual_close_price: float, predict_close_price: float):
    if actual_close_price > predict_close_price:
        return "sell"
    elif actual_close_price < predict_close_price:
        return "buy"
    else:
        return "hold"


def calculate_model_performance():
    global feats
    model = pickle.load(open("../model/best_model.pkl", "rb"))
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
        "r2_score": r2,
    }
    return performance_metrics


def get_price_history_from_db(
    start_time: str, end_time: str, interval: str, symbole: str = "BTC"
):
    global data
    df_price = data[["close_price"]]
    df_price.index = pd.to_datetime(df_price.index)
    filtered_data = df_price[start_time:end_time]
    resampled_data = filtered_data.resample(interval).last()
    price_history = resampled_data.to_dict()
    prices_data = []
    for date, price in price_history["close_price"].items():
        prices_data.append(
            {
                "symbol": "BTC",
                "interval": interval,
                "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "price": price,
            }
        )

    return prices_data


def calculate_moving_average(data: pd.DataFrame, window: int):
    return data["close_price"].rolling(window=window).mean()
