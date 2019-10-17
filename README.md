# Lyra scripts
Here are some of the scripts and functions we use in Lyra - open-source and free for you to use.

Note: We use discord.py 1.3.0a for Lyra, so we recommend you do the same.

## instance_picker.py
Allows users to run functions ("modules") on a specific instance they pick stored in a central database.

## uptime_calculator.py	
Calculates how long a Docker container has been up for based on its start date and and updates its uptime in a MySQL database. This is designed to calculate minutely uptime, so we recommend you run it on a minutely cron job (but it's not required).
