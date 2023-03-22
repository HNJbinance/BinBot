# Crypto Price Prediction API

Ce projet est une API pour la prédiction du prix de clôture des crypto-monnaies, en particulier le Bitcoin (BTC), en utilisant un modèle RandomForestRegressor pré-entraîné. L'API est construite avec FastAPI et utilise une base de données MySQL pour stocker les données historiques des prix. 

## Fonctionnalités

L'API offre les fonctionnalités suivantes :

1. Prédiction du prix de clôture pour la prochaine heure.
2. Consultation de l'historique des prix pour une période et une fréquence données.
3. Ajout d'un nouvel utilisateur (authentification requise).
4. Calcul et affichage des métriques de performance du modèle.

## Installation et configuration

### Prérequis

- Python 3.7 ou ultérieur
- MySQL

### Étapes d'installation

1. Clonez le dépôt GitHub :

```bash
git clone https://github.com/votre_nom_utilisateur/crypto-price-prediction.git

Accédez au répertoire du projet et créez un environnement virtuel :

cd crypto-price-prediction
python -m venv venv
