# Use the official Python image as the base image  
FROM python:latest 


# Set the working directory to /app  
WORKDIR /scripts
  
# Copy the requirements file into the container  
COPY scripts .  
  
# Install the requirements  
RUN  pip3 install -r requirements.txt --no-cache-dir
RUN sudo apt-get update && sudo apt-get -y install cron
COPY scripts/mycron /etc/cron.d/mycron  
RUN pip install uvicorn

ENV PATH="/root/.local/bin:${PATH}"  
# Set the file permissions on the cron job file  
RUN chmod 0644 mycron  
RUN crontab mycron
RUN touch /var/log/cron.log 
RUN chmod 0666 /var/log/cron.log  
EXPOSE 9000  


# Start the cron service  
#CMD ["bash", "-c", "python3 get_historical_data.py >> /var/log/cron.log  2>&1 & python3 get_stream_data.py >> /var/log/cron.log  2>&1 & cron && uvicorn healthcheck:app --host 0.0.0.0 --port 9000"]  
CMD ["bash", "-c", "python3 get_historical_data.py & python3 get_stream_data.py && uvicorn healthcheck:app --host 0.0.0.0 --port 9000"]  