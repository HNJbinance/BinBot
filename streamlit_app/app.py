import streamlit as st
import requests

# Titre de l'application
st.title("Prédiction de prix des crypto-monnaies")

# Formulaire pour récupérer les informations de l'utilisateur
symbol = st.text_input("Symbole de la crypto-monnaie (ex: BTC)")

# Bouton pour soumettre les informations et obtenir la prédiction
if st.button("Obtenir la prédiction"):
    # Remplacez cette URL par l'URL de votre API FastAPI
    api_url = "http://localhost:8000/predict"
    
    # Envoyer la requête à l'API
    response = requests.get(api_url, params={"symbol": symbol})

    # Afficher la prédiction reçue
    if response.status_code == 200:
        prediction = response.json()
        st.write(f"Prédiction pour {symbol}: {prediction['predicted_close_price']}")
    else:
        st.write(f"Erreur lors de la récupération de la prédiction: {response.status_code}")

