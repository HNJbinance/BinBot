# BinBot

BinBot est un projet qui récupère les données de streaming et historiques via l'API de Binance et Websocket. Il les charge dans une base de données montée sur MySQL. Pour ce faire, deux scripts get_historical_klines et get_stream_klines sont utilisés. Il y a deux tables dans la base de données : une table pour les données historiques et une table pour les données de streaming.

La base de données alimente une API montée avec FastAPI qui a un endpoint predict qui fait la prédiction sur la prochaine heure en se basant sur un modèle de machine learning Random Forest Regressor. Ensuite, il récupère le prix de streaming et renvoie un dictionnaire où il y a une décision d'achat ou de vente.

## Fonctionnalités

Récupération de données de streaming et historiques via l'API de Binance et Websocket.
Chargement des données dans une base de données MySQL.
Prédiction du prix de clôture pour la prochaine heure en utilisant un modèle Random Forest Regressor.
Endpoint API pour la prédiction et la décision d'achat ou de vente

## Installation et configuration

Avant d'installer BinBot, assurez-vous que les prérequis suivants sont installés :

Python 3.7 ou version ultérieure
Docker
Docker Compose

### Prérequis

- Python 3.7 ou ultérieur
- MySQL

### Étapes d'installation

#####1. Assurez-vous que votre système est à jour en exécutant les commandes suivantes :

```bash
sudo apt update && sudo apt upgrade
sudo apt install python3-pip
```
#####2. Vérifiez et installez Git :

```bash
git --version
sudo apt install git
```
#####3. Clonez le dépôt Git :

```bash
git clone https://github.com/HNJbinance/BinBot.git
cd BinBot
```
#####4. Construisez l'image Docker de votre application :

```bash
docker-compose build
```
#####5. Démarrez les conteneurs de votre application :

```bash
docker-compose up
```
#####6. Accédez à l'API via votre navigateur en allant à l'adresse suivante :

```bash
http://localhost:8000/docs
```
#####7. Pour supprimer les conteneurs précédemment créés :

```bash
docker-compose down
```

