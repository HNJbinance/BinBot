echo "stoping recent docker"
docker stop $(docker ps -aq) 

echo "activating virtualenv"
source ./binbotvenv/bin/activate 

echo "starting mysql container..."
docker start mysql_container
sleep 2

echo "starting get_historical_data.py in background..."
pkill -f get_historical_data.py
python3 get_historical_data.py  

echo "starting get_stream_data.py in background..."
pkill -f get_stream_data.py
python3 get_stream_data.py 
