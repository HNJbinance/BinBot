import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
# Chargement des données
data = pd.read_csv('binance_data.csv')
data.head()
data.info()
# Convert Open time and Close time to datetime format
data['Open time'] = pd.to_datetime(data['Open time'])
data['Close time'] = pd.to_datetime(data['Close time'])



# data = pd.get_dummies(data, columns=['Close time','Open time'])
#séparation des données en variables indépendantes et dépendantes
X = data.drop(['close_price'], axis=1)
y = data['close_price']

# Séparation des données en ensemble d'entraînement et ensemble de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  #Le paramètre drop permet d'éviter le problème de multicolinéarité

ohe = OneHotEncoder( drop="first", sparse=False)
ohe.fit_transform(X_train)
ohe.transform(X_test)
# Création du modèle Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)

# Entraînement du modèle
rf.fit(X_train, y_train)

# Prédiction sur l'ensemble de test
y_pred = rf.predict(X_test)

# Évaluation du modèle
print('Accuracy:', accuracy_score(y_test, y_pred))
