FROM python:3
  
# USER root  
WORKDIR /scripts
RUN apt-get update && apt-get install -y 
RUN pip install pandas fastapi matplotlib uvicorn 
RUN pip install apache-airflow
RUN airflow db init
RUN pip install requests  
RUN airflow users create -r Admin -u airflow -p airflow -f airflow -l airflow -e airflow@airflow.com
 
COPY /scripts/chart.py .
COPY /scripts/my_dag.py /usr/local/lib/python3.11/site-packages/airflow/example_dags/

CMD ["bash", "-c", "airflow scheduler & airflow webserver -p 8080 & uvicorn chart:app --host 0.0.0.0 --port 9090"]   