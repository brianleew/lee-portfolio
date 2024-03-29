""" Utility File For Working With Sessions """
# --- ABOUT ---
# db.py
# This utility class contains functions related to session handling.

## IMPORT DEPENDENCIES ##
from uuid import uuid4
from mysql.connector import Error
import arrow
import redis
from util import db

# Check session if session token exists in db and if it is valid return tuple (Status, Error)
def check_session(session_token):
    """ Checks Validity Of Session Token """
    cached = True
    ## CONNECT TO DATABASE ##
    if db.REDIS_AVAILABLE.wait(0.01):
        try:
            rdb = redis.Redis(host='db-cache', port=6379, decode_responses=True, db=0)
            result = rdb.get(session_token)
            rdb.close()
            if result is not None:
                print('using redis')
                return True, None
            cached = False
        except redis.exceptions.ConnectionError as err:
            print(f'Failed to connect to cache: {err}')

    try:
        conn = db.connect_db()
    except Error as e:
        return False, e
    ## OPEN CURSOR AND CHECK FOR SESSION ##
    with conn.cursor(dictionary=True) as cursor:
        try:
            cursor.execute('SELECT * FROM sessions WHERE session_id = %s', (session_token,))
            result = cursor.fetchone()
        except Error as err:
            conn.close()
            return False, err
    ## IS SESSION EXIST ##
    if result is None:
        conn.close()
        return False, 'Session Does Not Exist'
    ## IS SESSION EXPIRED ##
    if arrow.get(result['session_expire']) < arrow.utcnow():
        revoke_session(session_token)
        conn.close()
        return False, 'Session Expired'
    conn.close()
    # If session is not cached and redis server is up then cache the session
    if not cached and db.REDIS_AVAILABLE.wait(0.01):
        try:
            rdb = redis.Redis(host='db-cache', port=6379, decode_responses=True, db=0)
            session_expire = arrow.get(result['session_expire'])
            current_time = arrow.utcnow()
            ttl = min(int((session_expire - current_time).total_seconds()), 1800)
            rdb.setex(session_token, ttl, result['account_id'])
            rdb.close()
        except redis.exceptions.ConnectionError as err:
            print(f'Failed to connect to cache: {err}')
    return True, None

# Create a new session token, add it to db, and return tuple (Session Token, Error)
def grant_session(account_id):
    """ Creates A Session For Given Account """
    ## CONNECT TO DATABASE ##
    try:
        conn = db.connect_db()
    except Error as e:
        return None, e
    ## GENERATE SESSION UUID ##
    session_token = str(uuid4())
    ## CREATE CURSOR AND INSERT SESSION ##
    with conn.cursor() as cursor:
        try:
            sql = """
                INSERT INTO sessions (session_id, account_id, session_expire)
                VALUES (%s, %s, %s);
                """
            values = (session_token, account_id, (arrow.utcnow().shift(hours=3).datetime))
            cursor.execute(sql, values)
        except Error as err:
            conn.close()
            return None, err
        conn.commit()
    ## CLOSE AND RETURN SESSION TOKEN ##
    conn.close()
    if db.REDIS_AVAILABLE.wait(0.01):
        try:
            rdb = redis.Redis(host='db-cache', port=6379, decode_responses=True, db=0)
            rdb.setex(session_token, 1800, account_id)
            rdb.close()
        except redis.exceptions.ConnectionError as err:
            print(f'Failed to connect to cache: {err}')

    return session_token, None

# Remove specific session token from db returns (Status, Error)
def revoke_session(session_token):
    """ Removes Session From Database """
    ## CONNECT TO DATABASE ##

    if db.REDIS_AVAILABLE.wait(0.01):
        try:
            rdb = redis.Redis(host='db-cache', port=6379, decode_responses=True, db=0)
            rdb.delete(session_token)
            rdb.close()
        except redis.exceptions.ConnectionError as err:
            print(f'Failed to connect to cache: {err}')

    try:
        conn = db.connect_db()
    except Error as e:
        return False, e
    ## CREATE CURSOR AND DELETE SESSION ID##
    with conn.cursor() as cursor:
        try:
            cursor.execute('DELETE FROM sessions WHERE session_id = %s', (session_token,))
        except Error as err:
            conn.close()
            return False, err
        conn.commit()
    ## CLOSE AND RETURN SUCCESS ##
    conn.close()
    return True, None

# Get sessions data returns (Session Data, Error) #
def get_session_data(session_token):
    """ Get Session Data From Database """
    ## VALIDATE SESSION ##
    valid_session, err = check_session(session_token)
    if valid_session is False:
        return None, err
    ## CONNECT TO DATABASE ##

    if db.REDIS_AVAILABLE.wait(0.01):
        try:
            rdb_result = []
            rdb = redis.Redis(host='db-cache', port=6379, decode_responses=True, db=0)
            rdb_result.append(rdb.get(session_token))
            rdb_result.append(rdb.ttl(session_token))
            rdb.close()
            if len(rdb_result) != 0:
                print('using redis')
                return {
                    'account_id': int(rdb_result[0]),
                    'session_expire': arrow.utcnow().shift(seconds=int(rdb_result[1])).datetime
                    }, None
        except redis.exceptions.ConnectionError as err:
            print(f'Failed to connect to cache: {err}')

    try:
        conn = db.connect_db()
    except Error as e:
        return None, e
    ## CREATE CURSOR AND GET SESSION DATA ##
    with conn.cursor(dictionary=True) as cursor:
        try:
            cursor.execute('SELECT * FROM sessions WHERE session_id = %s', (session_token,))
            session_data = cursor.fetchone()
        except Error as err:
            conn.close()
            return None, err
    ## IF SESSION DATA EXISTS ##
    if session_data is None:
        conn.close()
        return None, 'No Session Associated with Session ID'
    ## CLOSE AND RETURN SESSION DATA
    conn.close()
    return session_data, None

# Remove expired tokens from db (Status, Error)
def cleanup_sessions():
    """ Removes All Expired Sessions From Database """
    ## CONNECT TO DATABASE ##

    if db.REDIS_AVAILABLE.wait(0.01):
        try:
            rdb = redis.Redis(host='db-cache', port=6379, decode_responses=True, db=0)
            rdb.flushdb(0)
            rdb.close()
        except redis.exceptions.ConnectionError as err:
            print(f'Failed to connect to cache: {err}')

    try:
        conn = db.connect_db()
    except Error as e:
        return False, e
    ## CREATE CURSOR AND DELETE EXPIRED SESSIONS ##
    with conn.cursor(dictionary=True) as cursor:
        try:
            cursor.execute('SELECT * FROM sessions WHERE session_expire < %s', (arrow.utcnow().datetime,))
            expired_sessions = cursor.fetchall()
        except Error as err:
            conn.close()
            return False, err
        for session in expired_sessions:
            try:
                cursor.execute(
                    'DELETE FROM sessions WHERE session_id = %s', (session['session_id'],)
                )
            except Error as err:
                conn.close()
                return False, err
        conn.commit()
    ## CLOSE AND RETURN SUCCESS ##
    conn.close()
    return True, None
