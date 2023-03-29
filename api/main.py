from functions import *
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    lastname: str
    login: str
    password: str

##############################################################################################################
#                                api
##############################################################################################################


# @api.post("/add_user/{id_api_users}")
# def add_user(
#     id_api_users: int,
#     name: str,
#     lastname: str,
#     login: str,
#     password: str,
#     username: str = Depends(get_current_username),
# ):
#     """
#     Ajoute un utilisateur à la base de données avec les informations fournies dans la requête.
#     Args:
#         id_api_users (int): L'ID de l'utilisateur à ajouter à la base de données.
#         name (str): Le nom de l'utilisateur à ajouter à la base de données.
#         lastname (str): Le nom de famille de l'utilisateur à ajouter à la base de données.
#         login (str): Le nom d'utilisateur de l'utilisateur à ajouter à la base de données.
#         password (str): Le mot de passe de l'utilisateur à ajouter à la base de données.
#         username (str): Le nom d'utilisateur actuel de l'utilisateur authentifié.

#     Returns:
#         Un dictionnaire contenant un message de confirmation et les informations de l'utilisateur ajouté.
#     """
#     add_user_to_db(id_api_users, name, lastname, login, password)
#     return {
#         "message": "User added successfully",
#         "name": name,
#         "lastname": lastname,
#         "login": login,
#         "password": password,
#     }

@api.post("/add_user/{id_api_users}")
def add_user(
    id_api_users: int,
    user: UserBase,
    username: str = Depends(get_current_username),
):
    """
    Ajoute un utilisateur à la base de données avec les informations fournies dans la requête.
    Args:
        id_api_users (int): L'ID de l'utilisateur à ajouter à la base de données.
        user (UserBase): Les informations de l'utilisateur à ajouter à la base de données.
        username (str): Le nom d'utilisateur actuel de l'utilisateur authentifié.

    Returns:
        Un dictionnaire contenant un message de confirmation et les informations de l'utilisateur ajouté.
    """
    add_user_to_db(id_api_users, **user.dict())
    return {
        "message": "User added successfully",
        **user.dict(),
    }
    

# @api.put("/users/{id_api_users}")
# def update_user(
#     id_api_users: int,
#     name: str,
#     lastname: str,
#     login: str,
#     password: str,
#     username: str = Depends(get_current_username),
# ):
#     """
#     Met à jour les informations d'un utilisateur dans la base de données avec les informations fournies dans la requête.
#     Args:
#         id_api_users (int): L'ID de l'utilisateur à mettre à jour dans la base de données.
#         name (str): Le nouveau nom de l'utilisateur à mettre à jour dans la base de données.
#         lastname (str): Le nouveau nom de famille de l'utilisateur à mettre à jour dans la base de données.
#         login (str): Le nouveau nom d'utilisateur de l'utilisateur à mettre à jour dans la base de données.
#         password (str): Le nouveau mot de passe de l'utilisateur à mettre à jour dans la base de données.
#         username (str): Le nom d'utilisateur actuel de l'utilisateur authentifié.

#     Returns:
#         Un dictionnaire contenant un message de confirmation et les informations de l'utilisateur mis à jour.
#     """
#     update_user_db(id_api_users, name, lastname, login, password)
#     return {
#         "message": "User updated successfully",
#         "name": name,
#         "lastname": lastname,
#         "login": login,
#         "password": password,
#     }

@api.put("/users/{id_api_users}")
def update_user(
    id_api_users: int,
    user: UserBase,
    username: str = Depends(get_current_username),
):
    """
    Met à jour les informations d'un utilisateur dans la base de données avec les informations fournies dans la requête.
    Args:
        id_api_users (int): L'ID de l'utilisateur à mettre à jour dans la base de données.
        user (UserBase): Les nouvelles informations de l'utilisateur à mettre à jour dans la base de données.
        username (str): Le nom d'utilisateur actuel de l'utilisateur authentifié.

    Returns:
        Un dictionnaire contenant un message de confirmation et les informations de l'utilisateur mis à jour.
    """
    update_user_db(id_api_users, **user.dict())
    return {
        "message": "User updated successfully",
        **user.dict(),
    }

@api.delete("/users/{id_api_users}")
def delete_user(id_api_users: int, username: str = Depends(get_current_username)):
    """
    Supprime un utilisateur de la base de données avec l'ID spécifié.
    Args:
        id_api_users (int): L'ID de l'utilisateur à supprimer de la base de données.
        username (str): Le nom d'utilisateur actuel de l'utilisateur authentifié.

    Returns:
        Un dictionnaire contenant un message de confirmation de la suppression de l'utilisateur.
    """
    delete_user_db(id_api_users)

    # Return a JSON response indicating that the user has been deleted
    return {"message": "User deleted successfully"}


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


@api.post("/retrain_model")
def retrain_model(username: str = Depends(get_current_username)):
    """
    Réentraîne le modèle de prédiction avec les données stockées dans la base de données.

    L'utilisateur doit être authentifié pour accéder à cette fonction.

    Retourne:
        Un dictionnaire contenant les informations suivantes:
        - message (str): Un message indiquant que l'entraînement du modèle s'est terminé avec succès.
    """
    global model, feats, target
    
    model = train_model(feats, target)

    return {"message": "Le modèle a été réentraîné avec succès."}
