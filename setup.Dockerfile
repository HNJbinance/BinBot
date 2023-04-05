FROM mysql:latest
# déplacer au docker compose après 

EXPOSE 3306
#Copie tous les scripts d'init vers le dossier de demarrage du service mysql (ils seront automatiquement exécutés)
COPY ./scripts/init_opa_database.sql /docker-entrypoint-initdb.d/