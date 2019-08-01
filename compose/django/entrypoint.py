import sys
import os
import time
import MySQLdb

def mysql_connected():
    try:
        conn = MySQLdb.connect(
            host=os.environ.get('MYSQL_LOCAL_HOST'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            connect_timeout=1
        )
        return True
    except MySQLdb._exceptions.OperationalError as error:
        print(error)
        return False

while True:
    print('Trying to connect')
    if mysql_connected():
        print('Database connected')
        break;

    print('Waiting for database to connect. Retrying')
    time.sleep(1)

