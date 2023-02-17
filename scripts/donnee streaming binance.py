import requests

# obtenir les données de cours en temps réel
url = "https://api.binance.com/api/v3/ticker/price"

# Envoyer une requête à l'API pour obtenir les données
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Convertir les données en forme de liste
    data = response.json()
    
    # Filtrer les données pour n'inclure que les paires de crypto-monnaies 
    # que nous sommes intéressés
    filtered_data = []
    for item in data:
        if item["symbol"].endswith("BTC"):
            filtered_data.append(item)
    
    # Enregistrer les données filtrées pour une utilisation ultérieure
    with open("filtered_api_data.json", "w") as file:
        file.write(str(filtered_data))
else:
    # Afficher un message d'erreur si la requête a échoué
    print("Error: La requête à l'API a échoué avec le code de statut {}".format(response.status_code))
