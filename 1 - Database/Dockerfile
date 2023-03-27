FROM mysql:latest 
# déplacer au docker compose après 

EXPOSE 3306
#Copie tous les scripts d'init vers le dossier de demarrage du service mysql (ils seront automatiquement exécutés)
COPY ./init_scripts /docker-entrypoint-initdb.d/