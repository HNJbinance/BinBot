FROM mysql:latest 
# déplacer au docker compose après 
ENV MYSQL_ROOT_PASSWORD=temp123  
# déplacer au docker compose après
ENV MYSQL_DATABASE=opa  
#Copie tous les scripts d'init vers le dossier de demarrage du service mysql (ils seront automatiquement exécutés)
COPY ./init_scripts /docker-entrypoint-initdb.d/