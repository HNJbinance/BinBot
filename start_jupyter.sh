echo starting jupyter notebook...
pkill -f jupyter-notebook
cd .. 
jupyter notebook --no-browser --ip="ec2-54-78-128-185.eu-west-1.compute.amazonaws.com" </dev/null &>/dev/null &

 