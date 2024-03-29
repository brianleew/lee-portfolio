# --- PROJECT ---
# 2023 CSC 4610-4620
# Demand Response Portal
# Evyn Price, Enora Boscher, Serena Labelle, Elijah Monroe, Mykola (Nick) Omelchenko,
# Shelby Smith, William Goodson, Won (Brian) Lee

""" Utility File For Connecting To Database """

# --- ABOUT ---
# db.py
# This utility class contains functions to integrate with the database.
from os import getenv
import time
import threading
from mysql.connector import connect, Error
from pythonping import ping

REDIS_AVAILABLE = threading.Event()

def connect_db():
    """ Gets Config And Returns Connection """

    db_config = {
        'host': getenv('DB_HOST'),
        'user': getenv('DB_USER'),
        'password': getenv('DB_PASSWORD'),
        'database': getenv('DB_DATABASE')
    }
    try:
        conn = connect(**db_config)
        return conn
    except Error as e:
        raise e

def test_cache_connection (event:threading.Event):
    """ Checks the connection to the cache server """
    while True:
        try:
            response = ping('db-cache', count=1, timeout=1)
            if response.success():
                event.set()
        except Exception as e:
            event.clear()
            print(f'Failed to connect {str(e)}')
        time.sleep(5)

def start_redis_check(event):
    """ Starts thread to always keep up with cache server status """
    redis_thread = threading.Thread(target=test_cache_connection, args=(event,))
    redis_thread.daemon = True
    redis_thread.start()
