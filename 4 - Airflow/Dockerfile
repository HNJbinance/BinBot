FROM apache/airflow:latest
  
USER root  
WORKDIR /scripts

RUN apt-get update && apt-get install -y \  
    && apt-get clean \  
    && rm -rf /var/lib/apt/lists/*  
  
RUN pip3 install requests  
RUN pip3 install apache-airflow
#wget https://dst-de.s3.eu-west-3.amazonaws.com/airflow_avance_fr/docker-compose/docker-compose.yamlRUN airflow users create --username airflow --password airflow --role Admin --email airflow@example.com --firstname test --lastname test
  
COPY /scripts/tasks_utils.py /usr/local/airflow/dags/  
COPY /scripts/mon_dag.py /usr/local/airflow/dags/

CMD ["airflow", "webserver", "-p", "8080"]  