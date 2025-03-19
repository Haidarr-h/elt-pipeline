#!/bin/bash

# Start the cron service in the background
cron

# Run the script immediately
python /app/elt_script.py

# Keep the container running and show the cron log
tail -f /var/log/cron.log
