# Use the official Python image as the base image  
FROM python:latest 

WORKDIR /trainapi
COPY ./models/model_opt_rfc.pkl ./models/model_opt_rfc.pkl

# definition du  working directory to /scripts ou y'aura tous les fichiers dans le conteneur docker
WORKDIR /scripts
  
# Copier tous les fichiers de la machine locale vers le working directory ou on travail celui du conteneur  
COPY ./scripts .  
# COPY ./models/model_opt_rfc.pkl ./models
# Install the requirements  
RUN  pip install -r requirement.txt --no-cache-dir
#mise à jour du  gestionnaire de paquets APT et installation du Cron
RUN apt-get update && apt-get -y install cron
#copier mycron dans le repeertoire du conteneur
COPY scripts/mycron /etc/cron.d/mycron  
RUN pip install uvicorn
#définir une variable d'environnement pour inclure le répertoire "/root/.local/bin" dans le chemin de recherche d'exécution
ENV PATH="/root/.local/bin:${PATH}"  
# Set the file permissions on the cron job file  
RUN chmod 0644 mycron  
RUN crontab mycron
#creation du  fichier de journalisation "cron.log" dans le répertoire "/var/log"
RUN touch /var/log/cron.log 
RUN chmod 0666 /var/log/cron.log  
EXPOSE 9000  


# Start the cron service 
#définir la commande par défaut qui sera exécutée lorsque le conteneur est démarré  
CMD ["bash", "-c", "uvicorn healthcheck:app --host 0.0.0.0 --port 9000 & cron & python3 get_historical_klines.py && python3 get_stream_klines.py "]  