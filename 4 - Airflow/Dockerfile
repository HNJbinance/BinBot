FROM python:3
  
# USER root  
WORKDIR /scripts
RUN apt-get update && apt-get install -y 
RUN pip install pandas fastapi matplotlib uvicorn 
#installation de apache airflow
RUN pip install apache-airflow
#initialisation de la base de sonnées airflow
RUN airflow db init
RUN pip install requests  
#creation d'un utilisateur avec le nom d'utilisateur "airflow" et le mot de passe "airflow"
RUN airflow users create -r Admin -u airflow -p airflow -f airflow -l airflow -e airflow@airflow.com
#copier chart et my-dag vers le repertoire du travail dans le conteneur du docker
COPY /scripts/chart.py .
COPY /scripts/my_dag.py /usr/local/lib/python3.11/site-packages/airflow/example_dags/

#lancer simultanément le planificateur et le serveur Web d'Apache Airflow, ainsi qu'une application FastAPI nommée "chart" 
CMD ["bash", "-c", "airflow scheduler & airflow webserver -p 8080 & uvicorn chart:app --host 0.0.0.0 --port 9090"]   