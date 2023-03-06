echo "stopping mysql container..."
docker stop mysql_container

echo "stopping get_stream_data.py ..."
pkill -f get_stream_data.py

echo "stopping get_historical_data.py ..."
pkill -f get_historical_data.py

echo "Done"


