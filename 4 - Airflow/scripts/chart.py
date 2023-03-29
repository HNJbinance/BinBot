import pandas as pd  
from fastapi import FastAPI  
from fastapi.responses import HTMLResponse  
import matplotlib.pyplot as plt  
from io import BytesIO  
import base64 
# Read the CSV file into a DataFrame  

# Create a FastAPI application  
app = FastAPI() 
# Define a route to display the chart  
@app.get('/chart', response_class=HTMLResponse)  
def chart(): 
    df = pd.read_csv('predictions.csv')  
    # Plot a scatter chart of Predicted Close Price vs Actual Price  
    fig, ax = plt.subplots()  
    ax.plot(df['Actual Time'], df['Actual Price'], label='Actual Price')  
    ax.plot(df['Actual Time'], df['Predicted Close Price'], label='Predicted Close Price')  
    ax.set_xlabel('Actual Time')  
    ax.set_ylabel('Price')  
    ax.set_title('la prediction du prix actuel')  
    ax.legend()  
    #Actual Price and Predicted Close Price Over Time  
      
    # Convert the chart to a base64-encoded string  pour l'utiliser pour afficher dans une page html
    buffer = BytesIO()  
    plt.savefig(buffer, format='png')  
    buffer.seek(0)  
    image_string = base64.b64encode(buffer.getvalue()).decode()  
      
    # Create an HTML page that displays the chart  
    #pour créer une page HTML qui affiche le graphique de dispersion
    page = f'''  
    <html>  
        <body>  
            <h1>Predicted Close Price vs Actual Price</h1>  
            <img src="data:image/png;base64,{image_string}">  
        </body>  
    </html>  
    '''  
    return page