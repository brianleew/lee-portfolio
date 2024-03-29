""" Utility File For Working With Users """

## IMPORT DEPENDENCIES ##
from bcrypt import gensalt, hashpw
from mysql.connector import Error

from util import db

def get_user_data(account_id):
    """ Gets User Data From Database """
    ## CONNECT TO DATABASE ##
    try:
        conn = db.connect_db()
    except Error as e:
        return None, e
    ## CREATE CURSOR AND GET USER DATA ##
    with conn.cursor(dictionary=True) as cursor:
        try:
            cursor.execute(
                """
                SELECT account_id, email, first_name, last_name, users.org_id,
                approval_status, organizations.org_name
                FROM users JOIN organizations
                ON users.org_id = organizations.org_id WHERE account_id = %s;
                """,
                (account_id,)
            )
            user_data = cursor.fetchone()
        except Error as err:
            conn.close()
            return None, err
    ## CHECK IF USER DATA IS EMPTY ##
    if user_data == {}:
        conn.close()
        return None, 'User does not exist'
    ## CLOSE AND RETURN USER DATA ##
    conn.close()
    return user_data, None

def update_user_data(account_id, req_data):
    """ Updates User Data """
    ## DEFINE ALLOWED UPDATE FIELDS AND NEEDED LISTS ##
    allowed_fields = ['first_name', 'last_name', 'email', 'password']
    fields = []
    values = []
    queries = []
    ## PARSE REQUEST ##
    ## IF PASSWORD UPDATE IS REQUESTED -> UPDATE PASSWORD (THIS MAY NEED TO BE MOVED) ##
    for field in allowed_fields:
        if field in req_data:
            fields.append(field)
            values.append(req_data[field])
    ## GENERATE SQL QUERIES ##
    for i, field in enumerate(fields):
        if field == 'password':
            queries.append(
                f"""
                UPDATE logins
                SET password_hash = '{(hashpw(values[i].encode(), gensalt())).decode()}'
                WHERE account_id = {account_id};
                """
            )
        else:
            queries.append(
                f"UPDATE users SET {field} = '{values[i]}' WHERE account_id = {account_id}"
            )
    ## CONNECT TO DATABASE ##
    try:
        conn = db.connect_db()
    except Error as e:
        return False, e
    ## CREATE CURSOR AND EXECUTE QUERIES ##
    with conn.cursor() as cursor:
        for query in queries:
            try:
                cursor.execute(query)
            except Error as e:
                conn.close()
                return False, e
        conn.commit()
    ## CLOSE AND RETURN SUCCESS ##
    conn.close()
    return True, None

def delete_user_data(account_id):
    """ Deletes User """
    ## CONNECT TO DATABASE ##
    try:
        conn = db.connect_db()
    except Error as e:
        return False, e
    ## CREATE CURSOR AND DELETE USER DATA ##
    with conn.cursor() as cursor:
        try:
            cursor.execute('DELETE FROM users WHERE account_id = %s', (account_id, ))
        except Error as e:
            conn.close()
            return False, e
        conn.commit()
    ## CLOSE AND RETURN SUCCESS ##
    conn.close()
    return True, None

def can_access_meter (account_id, meter_id):
    """ Checks If User Has Access To Specified Meter """
    # Prepared sql statements
    valid_meter = 'SELECT COUNT(*) FROM meters WHERE meter_id = %s'
    valid_entity_ids = 'SELECT entity_id FROM meter_map WHERE meter_id = %s'
    # Connect to db
    try:
        conn = db.connect_db()
    except Error as e:
        return False, e
    # Fetch valid entity ids
    with conn.cursor(dictionary=True) as cursor:
        # Check if meter id exists
        cursor.execute(valid_meter, (meter_id,))
        result = cursor.fetchone()
        if result['COUNT(*)'] != 1:
            return False, 'Invalid Meter'
        # Get valid ids
        user_data, _ = get_user_data(account_id)
        cursor.execute(valid_entity_ids, (meter_id,))
        results = cursor.fetchall()
    # Check if user account id is in valid ids
    entity_ids = [result['entity_id'] for result in results]
    if user_data['org_id'] is None:
        if user_data['account_id'] not in entity_ids:
            return False, 'Access Denied'
    # Check if user org  id is in valid ids
    else:
        if user_data['org_id'] not in entity_ids:
            return False, 'Access Denied'

    # FUTURE SPACE FOR CACHING CONNECTION IN DB=1

    # Return True if user can access meter
    return True, None

def get_user_org (account_id):
    """ Fetches User Org ID """
    user_data, err = get_user_data(account_id)
    if err is not None:
        return None, err
    return user_data['org_id'], None

def linked_meter_ids (account_id):
    """ Fetches Meter IDs Linked To User """
    user_data, err = get_user_data(account_id)
    if err is not None:
        return None, err
    get_meters = """
            SELECT meter_id FROM  meter_map WHERE entity_id = %s;
            """
    meter_ids = []
    # Connect to db
    try:
        conn = db.connect_db()
    except Error as e:
        return False, e

    with conn.cursor(dictionary=True) as cursor:
        if not user_data['org_id']:
            cursor.execute(get_meters, (user_data['account_id'],))
            meter_ids = [result['meter_id'] for result in cursor.fetchall()]
            return meter_ids, None
        else:
            cursor.execute(get_meters, (user_data['org_id'],))
            meter_ids = [result['meter_id'] for result in cursor.fetchall()]
            return meter_ids, None
    return None, "No meters found"