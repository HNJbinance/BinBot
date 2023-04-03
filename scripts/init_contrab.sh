BinBotDir=`ls -d $PWD/..`
echo $BinBotDir
echo "Schedule get_historical_data & get_stream_data every hours..."
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "*/30 * * * * python3 $BinBotDir/get_stream_data.py" >> mycron
echo "*/30 * * * * python3 $BinBotDir/get_historical_data.py" >> mycron
#install new cron file
crontab mycron
rm mycron
echo Done !
