from datetime import datetime, timedelta  
import csv  
import requests  
import os 
from airflow import DAG  
from airflow.operators.python_operator import PythonOperator

api_host = os.getenv('API_HOST', 'localhost')  
username = os.getenv('API_USERNAME','')  
password = os.getenv('API_PASSWORD','')  
def call_api_and_write_to_csv():  
    # Set up authentication credentials  
    auth = requests.auth.HTTPBasicAuth(username, password) 
    api_url = f"http://{api_host}:8000/predict"  
    # Make API request with authentication    
    response = requests.get(api_url, auth=auth)     
    if response.status_code != 200:  
        raise Exception("Failed to call API")  
    data = response.json()  
  
    # Write data to CSV file  
    filename = "predictions.csv"  
    file_exists = os.path.isfile(filename)  
    with open(filename, mode="a", newline="") as file:  
        writer = csv.writer(file)  
        if not file_exists:  
            writer.writerow([  
                "Symbol",  
                "Interval",  
                "Actual Time",  
                "Actual Price",  
                "Next Hour",  
                "Predicted Close Price",  
                "Decision",  
            ])  
        writer.writerow([  
            data["symbol"],  
            data["interval"],  
            data["actual_time"],  
            data["actual_price"],  
            data["next_hour"],  
            data["predicted_close_price"],  
            data["decision"],  
        ])
  
    print('API call successful')  
     
default_args = {  
    'owner': 'me',  
    'depends_on_past': False,  
    'start_date': datetime(2021, 8, 1),  
    'retries': 1,  
    'retry_delay': timedelta(minutes=2)  
}  
  
dag = DAG(  
    'my_dag',  
    default_args=default_args,  
    description='Call API every 5 minutes and write to CSV',  
    schedule_interval=timedelta(minutes=5)  
)  
  
task = PythonOperator(  
    task_id='call_api_and_write_to_csv',  
    python_callable=call_api_and_write_to_csv,  
    dag=dag  
)  
task
