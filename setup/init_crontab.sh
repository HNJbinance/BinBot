BinBotDir=`ls -d $PWD/..`
echo $BinBotDir
echo Schedule get_historical_data.py every hours...
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "*/10 * * * * python3 $BinBotDir/purge_stream_data.py" >> mycron
echo "5 * * * * python3 $BinBotDir/get_stream_data.py" >> mycron
echo "10 * * * * python3 $BinBotDir/get_historical_data.py" >> mycron
#install new cron file
crontab mycron
rm mycron
echo Done !
