from datetime import datetime, timedelta  
from airflow import DAG  
from airflow.operators.python_operator import PythonOperator  
from functions import predict_close_price, retrain_model  
  
default_args = {  
    'owner': 'airflow',  
    'depends_on_past': False,  
    'start_date': datetime(2022, 1, 1),  
    'email_on_failure': False,  
    'email_on_retry': False,  
    'retries': 1,  
    'retry_delay': timedelta(minutes=5),  
}  
  
dag = DAG(  
    'crypto_prediction',  
    default_args=default_args,  
    description='DAG pour prédire le prix de clôture des crypto-monnaies',  
    schedule_interval=timedelta(hours=1),  
)  

predict_task = PythonOperator(  
    task_id='predict_close_price',  
    python_callable=predict_close_price,  
    dag=dag,  
)  
  
retrain_task = PythonOperator(  
    task_id='retrain_model',  
    python_callable=retrain_model,  
    dag=dag,  
)  
  
predict_task >> retrain_task  
