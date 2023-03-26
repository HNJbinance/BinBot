import mysql.connector  
from fastapi import FastAPI  
  
app = FastAPI()  
  
@app.get('/healthcheck')  
def healthcheck():  
    try:  
        cnx = mysql.connector.connect(user='root', password='temp123', host='localhost', database='opa')  
        cursor = cnx.cursor()  
        cursor.execute('SELECT COUNT(*) FROM historical_klines')  
        result1 = cursor.fetchone()  
        cursor.execute('SELECT COUNT(*) FROM stream_klines')  
        result2 = cursor.fetchone()  
  
        if result1[0] > 0 and result2[0] > 0:  
            return {'status': 'ok'}  
        else:  
            return {'status': 'error', 'message': 'No data found'}  
    except mysql.connector.Error as err:  
        return {'status': 'error', 'message': str(err)}  