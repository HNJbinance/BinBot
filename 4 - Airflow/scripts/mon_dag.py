from datetime import datetime, timedelta  
from airflow import DAG  
from airflow.operators.python_operator import PythonOperator  
from tasks_utils import call_api_and_write_to_csv  
  
default_args = {  
    'owner': 'me',  
    'depends_on_past': False,  
    'start_date': datetime(2021, 8, 1),  
    'retries': 1,  
    'retry_delay': timedelta(minutes=5)  
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
