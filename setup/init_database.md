########################################
# ON NEW MACHINE ONYL
########################################
https://cloudcone.com/docs/article/how-to-install-docker-on-ubuntu-22-04-20-04/


########################################
# INSTALL AND RUN MYSQL DOCKER
########################################
docker pull mysql
docker run --name mysql_container -h 127.0.0.1 -p 3306:3306 -d -e MYSQL_ROOT_PASSWORD=temp123 mysql


########################################
# CREATING DATABASE & PERMISSIONS
########################################
docker exec -it mysql_container bash 
mysql -u root -ptemp123 

# Then copy paste the init_opa_database.sql


########################################
# reinstall OpenSSl
########################################
sudo rm -rf /usr/lib/python3/dist-packages/OpenSSL
sudo pip3 install pyopenssl
sudo pip3 install pyopenssl --upgrade

########################################
# install python requirements
########################################
pip install -r requirements.txt 

########################################
# init crontab
########################################
./init_crontab.sh

########################################
# Launch stream and historical script 
########################################
# Come back to BinBot/ then launch start.sh
cd ..
chmod 755 *.sh
./start.sh

