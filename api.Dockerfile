FROM python:latest


WORKDIR /trainapi 
# Copier les fichiers de code source dans le conteneur  
COPY ./scripts ./scripts 
COPY ./models ./models 
COPY ./requirements.txt .
RUN pip install uvicorn

ENV PATH="/root/.local/bin:${PATH}"  
# Installer les dépendances du projet  
RUN pip install -r requirements.txt  
  
# Définir le port de l'api

EXPOSE 8000

#pour garder/persister le model .pkl au cas ou le container s'arrête.
# VOLUME ./models

WORKDIR /trainapi/scripts
# Exécuter le script Python  
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]  
