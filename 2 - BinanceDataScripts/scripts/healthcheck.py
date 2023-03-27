import mysql.connector  
from fastapi import FastAPI, HTTPException  
from fastapi.responses import JSONResponse  
import os
app = FastAPI()  
  
@app.get('/healthcheck')  
def healthcheck():  
    try:  
        cnx = mysql.connector.connect(user='root', password=os.environ.get("MYSQL_PASSWORD"), host=os.environ.get("MYSQL_HOST"), database='opa')  
        cursor = cnx.cursor()  
        cursor.execute('SELECT COUNT(*) FROM historical_klines')  
        result1 = cursor.fetchone()  
        cursor.execute('SELECT COUNT(*) FROM stream_klines')  
        result2 = cursor.fetchone()  
  
        if result1[0] > 0 and result2[0] > 0:  
            return {'status': 'ok'}  
        else:  
            raise HTTPException(status_code=400, detail='No data found')  
    except mysql.connector.Error as err:  
        return JSONResponse(content={'status': 'error', 'message': str(err)}, status_code=400)  