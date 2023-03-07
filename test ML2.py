import pandas as pd
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

# Récupération des données à partir de l'API Binance
response = requests.get('https://api.binance.com/api/v3/klines',
                         params={'symbol': 'BTCUSDT', 'interval': '1d'})
data = response.json()

# Conversion des données en DataFrame pandas
df = pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 
                                 'Volume', 'Close time', 'Quote asset volume', 
                                 'Number of trades', 'Taker buy base asset volume', 
                                 'Taker buy quote asset volume', 'Ignore'])

# Conversion des timestamps en date
df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')

# Renommer les colonnes pour une meilleure compréhension
df.rename(columns={'Open': 'open_price', 'Close': 'close_price', 'Volume': 'volume'},
          inplace=True)

# Supprimer les colonnes inutiles
df.drop(columns=['High', 'Low', 'Quote asset volume', 'Number of trades',
                 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'], 
        inplace=True)

# Création de la variable cible
df['target'] = (df['close_price'].shift(-1) > df['close_price']).astype(int)

# Suppression de la dernière ligne pour éviter les valeurs nulles
df.drop(df.tail(1).index, inplace=True)

# Définition des features et de la variable cible
X = df[['open_price', 'close_price', 'volume']]
y = df['target']

# Séparation des données en ensemble d'entraînement et ensemble de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Entraînement du modèle RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rfc.fit(X_train, y_train)

# Prédictions sur l'ensemble de test
y_pred = rfc.predict(X_test)

# Évaluation de la performance du modèle
accuracy = accuracy_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred)
print('Accuracy: {:.2f}'.format(accuracy))
print('Recall: {:.2f}'.format(recall))
print('ROC AUC: {:.2f}'.format(roc_auc))

# Prédiction d'achat ou de vente
current_data = [[df['open_price'].iloc[-1], df['close_price'].iloc[-1], df['volume'].iloc[-1]]]
prediction = rfc.predict(current_data)[0]

if prediction == 1:
    print('Il est recommandé d\'acheter.')
else:
    print('Il n\'est pas recommandé d\'acheter.')

# Stratégie de vente
profit_threshold = 1.05 # Seuil de profit à 5%
loss_threshold = 0.95 # Seuil de perte à 5%
