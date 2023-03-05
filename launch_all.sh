echo "starting mysql container..."
docker restart mysql
sleep 2

echo "starting get_stream_data.py in background..."
pkill -f get_stream_data.py
python3 /home/ubuntu/datascientest/000-project/OPA/BinBot/get_stream_data.py </dev/null &>/dev/null &

echo "starting get_historical_data.py in background..."
pkill -f get_historical_data.py
python3 /home/ubuntu/datascientest/000-project/OPA/BinBot/get_historical_data.py  </dev/null &>/dev/null &


