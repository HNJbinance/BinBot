from functions import *


##############################################################################################################
#                                api
##############################################################################################################


@api.post("/add_user/{id_api_users}/{name}/{lastname}/{login}/{password}")
def add_user(id_api_users: int,
    name: str,
    lastname: str,
    login: str,
    password: str,
    username: str = Depends(get_current_username),
):
    add_user_to_db(id_api_users, name, lastname, login, password)
    return {
        "message": "User added successfully",
        "name": name,
        "lastname": lastname,
        "login": login,
        "password": password,
    }

@api.put("/users/{id_api_users}")
def update_user(id_api_users: int, name: str, lastname: str, login: str, password: str, username: str = Depends(get_current_username)):
    update_user_db(id_api_users, name, lastname, login, password)
    return {
        "message": "User updated successfully",
        "name": name,
        "lastname": lastname,
        "login": login,
        "password": password,
    }

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
    return {
        "symbol": "BTC/USDT",
        "interval": "1h",
        "actual_time": actual_time,
        "actual_price": close_price_stream,
        "next_hour": next_hour.strftime("%Y-%m-%d %H:%M:%S"),
        "predicted_close_price": round(next_hour_close_price, 2),
        "decision": decision(close_price_stream, next_hour_close_price),
    }


@api.get("/price_history/{start_time}/{end_time}/{interval}/{symbol}")
def get_price_history(
    start_time: str,
    end_time: str,
    interval: str,
    symbol: str = "BTC",
    username: str = Depends(get_current_username),
):
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
def get_moving_averages(
    symbol: str,
    interval: str,
    window: int,
    username: str = Depends(get_current_username),
):
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

    resampled_data = data[["close_price"]].resample(interval).last()
    moving_averages = calculate_moving_average(resampled_data, window)

    moving_averages_data = []
    for date, value in moving_averages.items():
        moving_averages_data.append(
            {
                "symbol": symbol,
                "interval": interval,
                "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "moving_average": value,
            }
        )

    return moving_averages_data
