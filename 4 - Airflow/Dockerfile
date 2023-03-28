FROM python:3
  
# USER root  
WORKDIR /scripts
ENV API_HOST=api
RUN apt-get update && apt-get install -y 
RUN pip install apache-airflow
RUN airflow db init
RUN pip install requests  
RUN airflow users create -r Admin -u airflow -p airflow -f airflow -l airflow -e airflow@airflow.com
 
COPY /scripts/tasks_utils.py /usr/local/lib/python3.11/site-packages/airflow/example_dags/  
COPY /scripts/my_dag.py /usr/local/lib/python3.11/site-packages/airflow/example_dags/

CMD ["bash", "-c", "airflow scheduler & airflow webserver -p 8080 && tail -f /scripts/predictions.csv"]   