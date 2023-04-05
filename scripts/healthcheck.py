import mysql.connector  
from fastapi import FastAPI, HTTPException  
from fastapi.responses import JSONResponse  
import os
app = FastAPI()  
  
@app.get('/healthcheck')  
def healthcheck():  
    try:  
        cnx = mysql.connector.connect(user='root', password=os.environ.get("MYSQL_PASSWORD"), host=os.environ.get("DB_HOST"), database='opa')  
        cursor = cnx.cursor()  
        cursor.execute('SELECT COUNT(*) FROM historical_klines')  
        result1 = cursor.fetchone()  
        cursor.execute('SELECT COUNT(*) FROM stream_klines')  
        result2 = cursor.fetchone()  
  
        if result1[0] > 0 and result2[0] > 0:  
            return {'status': 'ok', 'historical_count': result1[0],'stream_count':result2[0]   }  
        else:  
            raise HTTPException(status_code=400, detail='les données ne sont pas encore insérées !')  
    except mysql.connector.Error as err:  
        return JSONResponse(content={'status': 'error', 'message': str(err)}, status_code=400)  

#point d'extremité /helthcheck   et c'est un script de santé et de verification de l'etat des applications      