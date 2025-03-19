FROM python:3.8-slim

# Install PostgreSQL client and cron
RUN apt-get update && apt-get install -y postgresql-client-15 cron

# Copy files to the container
COPY start.sh /app/start.sh
COPY elt_script.py .

WORKDIR /app

# Add the cron job to crontab
RUN echo "0 3 * * * python /app/elt_script.py >> /var/log/cron.log 2>&1" | crontab -

# Make start.sh executable
RUN chmod +x /app/start.sh

# Use start.sh to start cron service
CMD ["/bin/sh", "/app/start.sh"]
