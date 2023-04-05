# BinBot

BinBot est un projet open-source qui vise à prédire le prix de clôture des crypto-monnaies, en particulier le Bitcoin (BTC), en utilisant des données de streaming et historiques provenant de l'API de Binance et Websocket. Les données sont stockées dans une base de données MySQL et alimentent une API montée avec FastAPI. Le modèle de machine learning utilisé est un Random Forest Regressor et est entrainé par la méthode des hyperparamètres. L'API offre plusieurs fonctionnalités, y compris la prédiction du prix de clôture pour la prochaine heure et compare avec le prix stream pour renvoyer une décision d'achat ou de vente selon votre position.

BinBot utilise une architecture basée sur des conteneurs (containers) pour faciliter le déploiement et la gestion du projet. Les conteneurs sont gérés par Docker Compose et incluent un container pour l'initialisation de la base de données et la définition des schémas, un container pour la base de données MySQL, un container pour la population de la base de données et les scripts, et un container pour l'API. Un volume contenant un fichier sql_properties.py est partagé entre les conteneurs.

Le projet est accompagné d'un guide d'installation détaillé pour faciliter la mise en place de l'application. Les utilisateurs peuvent également configurer des tâches CRON pour l'exécution automatique des scripts get_historical_klines et get_stream_klines.

Nous espérons que BinBot sera utile pour ceux qui s'intéressent à la prédiction des prix de crypto-monnaies et nous sommes ouverts à tout feedback ou contribution à ce projet.

## Schéma de l'architecture de BinBot

![Schéma de l'architecture de BinBot](https://raw.githubusercontent.com/HNJbinance/BinBot/main/schema_binbot.png)

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

1. Assurez-vous que votre système est à jour en exécutant les commandes suivantes :

```bash
sudo apt update && sudo apt upgrade
sudo apt install python3-pip
```
2. Vérifiez et installez Git :

```bash
git --version
sudo apt install git
```
3. Clonez le dépôt Git :

```bash
git clone https://github.com/HNJbinance/BinBot.git
cd BinBot
```
4. Construisez l'image Docker de votre application :

```bash
docker-compose build
```
5. Démarrez les conteneurs de votre application :

```bash
docker-compose up
```
6. Accédez à l'API via votre navigateur en allant à l'adresse suivante :

```bash
http://localhost:8000/docs
```
7. Pour supprimer les conteneurs précédemment créés :

```bash
docker-compose down
```

### Versions :

Version 1.0.0 : fonctionnalités de base comprenant la récupération des données de streaming et historiques via l'API de Binance et Websocket, l'entraînement d'un modèle Random Forest Regressor pour la prédiction du prix de clôture, et la création d'une API avec FastAPI pour la prédiction et la décision d'achat ou de vente.

Version 1.1.0 (à venir) : ajout de fonctionnalités supplémentaires telles que la consultation de l'historique des prix pour une période et une fréquence données, l'ajout d'un nouvel utilisateur avec authentification requise, et le calcul et l'affichage des métriques de performance du modèle.

Version 1.2.0 (à venir) : création d'un dashboard avec Streamlit pour visualiser les données de streaming en temps réel et l'état des prédictions.

Version 1.3.0 (à venir) : possibilité de lier le bot avec un compte Binance pour permettre des transactions en direct.



### Auteurs :

Hamza Ennaji
Ilham Noumir
Loic Montagnac
Souhila Lebib
