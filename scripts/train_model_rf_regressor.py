import pandas as pd
import numpy as np
import modules.sql_properties as sql
import mysql.connector
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import make_scorer
from sklearn.model_selection import RandomizedSearchCV, train_test_split, StratifiedKFold
from sklearn.model_selection import cross_val_score, GridSearchCV
import pickle


################################################################################################################
################################### Récupération des données de la DB ##########################################


sql = sql.SqlAction()
feats , target =sql.retrieve_historical_klines_dataframe()

  

################################################################################################################
################################### Préparation des données pour l'entrainement ################################
X_train, X_test, y_train, y_test = train_test_split(feats, target, test_size=0.2, random_state=42)

print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)
    

    
################################################################################################################
########################################### Recherche des hyperparamètres  #####################################
param_grid = {
    'n_estimators': [100],
    'max_depth': [None],
    'min_samples_split': [2],
    'min_samples_leaf': [2]
}

# param_grid = {
#         'n_estimators': [10, 50, 100, 200, 300, 400, 500],
#         'max_depth': [None] + list(np.arange(2, 20, 1)),
#         'min_samples_split': np.arange(2, 20, 1),
#         'min_samples_leaf': np.arange(1, 20, 1),
#         'max_features': ['auto', 'sqrt', 'log2', None] + list(np.arange(0.1, 1.1, 0.1)),
#         'bootstrap': [True, False],
#         'warm_start': [True, False],
#         'criterion': ['mse', 'mae']}

rf_model = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', verbose=2, n_jobs=-1)
start_time = time.time()
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

print("Le temps d'éxécution: ", time.time() - start_time )
print("Best model parameters: ", grid_search.best_params_)
print("Best model score: ",  grid_search.best_score_)

################################################################################################################
################################## Métriques et enregistrement du modèle  ######################################

pickle.dump(best_model,open('/mnt/models/model_opt_rfc.pkl','wb'))

train_preds = best_model.predict(X_train)
test_preds = best_model.predict(X_test)


train_rmse = np.sqrt(mean_squared_error(y_train, train_preds))
test_rmse = np.sqrt(mean_squared_error(y_test, test_preds))

print(f"RMSE pour l'ensemble d'entraînement: {train_rmse}")
print(f"RMSE pour l'ensemble de test: {test_rmse}")

