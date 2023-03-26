import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from scipy.stats import boxcox
import warnings
warnings.filterwarnings('ignore')
from sklearn.metrics import mean_squared_error



from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import pickle

data=pd.read_csv('data.csv')
data['close_time'] = pd.to_datetime(data['close_time'], unit='ms')
data = data.set_index('close_time')
data.sort_index(inplace = True)
data.columns

#fill any missing values
data = data.ffill()
# Drop any rows with missing values
data.dropna(inplace=True)

##Create lagged features for the Random Forest model for each column 

lag_columns = ['open_price', 'high_price', 'low_price', 'close_price', 'volume', 
               'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 
               'taker_buy_quote_asset_volume']

lag_count = 6

for col in lag_columns:
    for lag in range(1, lag_count + 1):
        data[f'{col}_lag{lag}'] = data[col].shift(lag)
data['next_close_price'] = data['close_price'].shift(-1)
# Supprimer les lignes avec des valeurs manquantes après la création des colonnes décalées
data.dropna(inplace=True)

# Récupérer les noms de colonnes
column_names = data.columns

# Afficher les noms de colonnes avec une numérotation
for idx, col_name in enumerate(column_names, 1):
    print(f"{idx}. {col_name}")

# Supprimer les colonnes indésirables pour les fonctionnalités
feats = data.drop(['close_price', 'id_symint', 'open_time'], axis=1)

# Utiliser la colonne 'close_price' comme cible
target = data['next_close_price']

# Pourcentage des données à utiliser pour l'ensemble de test (par exemple, 20%)
test_size = 0.2

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(feats, target, test_size=test_size, random_state=42)

# Définir les hyperparamètres à tester
param_grid = {
    'n_estimators': [10, 50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Créer une instance du modèle RandomForestRegressor
rf_model = RandomForestRegressor(random_state=42)

# Créer une instance de GridSearchCV pour rechercher les meilleurs hyperparamètres
grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', verbose=2, n_jobs=-1)

# Effectuer la recherche des meilleurs hyperparamètres en utilisant la validation croisée
grid_search.fit(X_train, y_train)

# Récupérer le meilleur modèle
best_model = grid_search.best_estimator_

print("Best model parameters: ", grid_search.best_params_)
print("Best model MSE: ", -grid_search.best_score_)

# Assuming your trained model is named `model`
with open("best_model.pkl", "wb") as file:
    pickle.dump(best_model, file)

# Faire des prédictions sur les ensembles d'entraînement et de test
train_preds = best_model.predict(X_train)
test_preds = best_model.predict(X_test)

# Calculer les métriques d'évaluation (RMSE)
train_rmse = np.sqrt(mean_squared_error(y_train, train_preds))
test_rmse = np.sqrt(mean_squared_error(y_test, test_preds))

print(f"RMSE pour l'ensemble d'entraînement: {train_rmse}")
print(f"RMSE pour l'ensemble de test: {test_rmse}")

with open("metrics.txt", "w") as f:
    f.write(f"RMSE pour l'ensemble d'entraînement: {train_rmse}\n")
    f.write(f"RMSE pour l'ensemble de test: {test_rmse}\n")
