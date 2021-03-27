### uptime_calculator.py: Calculates how long a Docker container has been up for based on its start date and and updates its uptime in a MySQL database.
### This is designed to calculate minutely uptime, so we recommend you run it on a minutely cron job (but it's not required).
### Created by Cam Cuozzo (@camcuozzo on Github)
### This script is used as one of the functions in the back-end script for Lyra.

import docker
import datetime
import pytz # https://pypi.org/project/pytz/
from dateutil import parser # https://pypi.org/project/python-dateutil/
import mysql.connector

client = docker.from_env()
mysql_connection = mysql.connector.connect(user='YOURUSER', password='YOURPASSWORD', database='YOURDATABASE')
cursor = mysql_connection.cursor()
utc = pytz.UTC

def uptime(container):
    startTime = parser.isoparse(container.attrs['State']['StartedAt']) # Getting the start date and time of the container in a parsable format
    uptime = utc.localize(datetime.datetime.now()) - startTime # Calculating uptime as a time object
    uptime_mins = uptime.seconds/60 # seconds is an attribute of time objects but minutes is not, so we make a minute variable ourselves
    
    # Updating the uptime in MySQL
    cursor.execute("UPDATE instances SET uptime = %s WHERE container_id = %s", (str(uptime_mins), str(container.id))) 
    mysql_connection.commit()

    # Useful to have logs :)
    print("Uptime refreshed.")

# Run the uptime function for every container we have running in Docker
for container in client.containers.list():
    uptime(container)
