""" Route For Interacting With Meters """
import arrow
from flask import Blueprint, jsonify, request, make_response
from mysql.connector import Error

from util import db
from util import users
from util import session

meters = Blueprint('meters', __name__, url_prefix='/api/entity/meters')
# EXPECT JSON BODY { id: <org_id or account_id>, meters: [] }

# --- Get Meters API Call ---
# This call will return a list of meters that the user has access to.
# The call will take the following arguments in the cookie:
# strSessionID: The session ID of the user
# The call will return the following JSON object:
# {
    # "ResponseType": "Success",
    # "Details": [
    #    {
    #        "meterID": "1",
    #       "lastUpdated": "2020-04-20 00:00:00",
    #       "lastUpdatedRelative": "2 days ago"
    #   },
    #   ]
# }
#
# If there is an error, the call will return the following JSON object:
# {
    # "ResponseType": "Error",
    # "Message": "Error message here"
# }
@meters.route('/', methods=['GET'])
def view_meters():
    """ Fetch All Meter Accessible To User """
    # Fetch the session ID from the cookie.
    session_id = request.cookies.get('strSessionID')
    if session_id is None:
        # If the session ID is not provided, return an error.
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Session cookie does not exist.'
                }))
        return response, 400

    # Attempt to connect to the database.
    try:
        conn = db.connect_db()
    except Error as e:
        response = make_response(
            jsonify(
                {'ResponseType': 'Error',
                 'Message': 'Could not create a connection to the database.',
                 'Details': e
                }))
        return response, 500

    with conn.cursor(dictionary=True) as cursor:
        # Prepared sql statement gets account id and org id for provided session
        str_prep_sql = """
            SELECT sessions.account_id, users.org_id
            FROM sessions
            JOIN users on sessions.account_id = users.account_id
            WHERE sessions.session_id = %s;
            """
        cursor.execute(str_prep_sql, (session_id,))
        result = cursor.fetchone()
        # If there are no results we return an error
        if result is None:
            conn.close()
            response = make_response(
                jsonify({
                    'ResponseType': 'Error',
                    'Message': 'Unable to find session ID'
                }))
            return response, 400

        # Response is in format [account_id, org_id]
        account_id = result['account_id']
        org_id = result['org_id']

        # Fetch meter map information for users organization, or users account id if residential
        str_prep_sql = """
            SELECT meter_map.entity_id, A.meter_id, A.last_updated
            FROM meter_map LEFT JOIN (SELECT meter_id, max(end_time) AS last_updated
            FROM meter_data group by meter_id) AS A ON meter_map.meter_id = A.meter_id WHERE entity_id = %s;
            """
        if org_id is None:
            cursor.execute(str_prep_sql, (account_id,))
        else:
            cursor.execute(str_prep_sql, (org_id,))

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        array = []
        for record in result:
            # Convert last updated time to relative time
            try:
                relative_time = arrow.get(record['last_updated']).humanize()
            except TypeError:
                relative_time = "Never"
            meter_object = {
                "meterID": record['meter_id'],
                "lastUpdated": record['last_updated'],
                "lastUpdatedRelative": relative_time
                }
            array.append(meter_object)

    response = make_response(
        jsonify({
            'ResponseType': 'Success',
            'Details': array
            }))
    return response, 200

@meters.route('/add', methods=['POST'])
def add_meter():
    """ Add Meter To Database """
    # Get session id
    session_id = request.cookies.get('strSessionID')
    if session_id is None:
        # If the session ID is not provided, return an error.
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Session cookie does not exist.'
                }))
        return response, 400  # Bad Request
    # Verify permissions
    session_data, err = session.get_session_data(session_id)
    if err is not None:
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': f'Session is invalid: {err}'
                }))
        return response, 401  # Unauthorized
    user_data, err = users.get_user_data(session_data['account_id'])
    if err is not None:
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': f'Unable to find user data: {err}'
                }))
        return response, 406  # Not Acceptable
    if user_data['org_id'] != 1:
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Invalid permissions'
                }))
        return response, 401  # Unauthorized
    if user_data['approval_status'] != 'Admin':
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Invalid permissions'
                }))
        return response, 401  # Unauthorized

    # Parse request
    req = request.get_json(silent=True)
    if req is None or (isinstance(req, dict) and not req):
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Missing required arguments.'
                }))
        return response, 400  # Bad Request
    if not req['meters']:
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Missing required arguments.'
                }))
        return response, 400  # Bad Request

    # Attempt to connect to the database.
    try:
        conn = db.connect_db()
    except Error as e:
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Could not create a connection to the database.',
                'Details': e
                }))
        return response, 500  # Internal Server Error

    check_meter_exists = 'SELECT COUNT(*) FROM meters WHERE meter_id = %s'
    insert_meter = 'INSERT INTO meters (meter_id) VALUES (%s)'
    with conn.cursor() as cursor:
        for meter in req['meters']:
            cursor.execute(check_meter_exists, (meter,))
            result = cursor.fetchone()[0]
            if result != 0:
                response = make_response(
                    jsonify({
                        'ResponseType': 'Error',
                        'Message': 'One or more meters already exist'
                        }))
                return response, 400  # Bad Request
            try:
                cursor.execute(insert_meter, (meter,))
            except Error as err:
                response = make_response(
                    jsonify({
                        'ResponseType': 'Error',
                        'Message': f'Unable to add meter: {err}'
                        }))
                return response, 400  # Bad Request
        conn.commit()
        response = make_response(
            jsonify({
                'ResponseType': 'Success',
                'Message': 'Meters were added successfully'
                }))
        return response, 200  # OK


@meters.route('/assign', methods=['POST'])
def assign_meters():
    """ Assign Meters To Specified ID """
    # Get session id
    session_id = request.cookies.get('strSessionID')
    if session_id is None:
        # If the session ID is not provided, return an error.
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Session cookie does not exist.'
                }))
        return response, 400  # Bad Request
    # Verify permissions
    session_data, err = session.get_session_data(session_id)
    if err is not None:
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': f'Session is invalid: {err}'
                }))
        return response, 401  # Unauthorized
    user_data, err = users.get_user_data(session_data['account_id'])
    if err is not None:
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': f'Unable to find user data: {err}'
                }))
        return response, 406  # Not Acceptable
    if user_data['org_id'] != 1:
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Invalid permissions'
                }))
        return response, 401  # Unauthorized
    if user_data['approval_status'] != 'Admin':
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Invalid permissions'
                }))
        return response, 401  # Unauthorized
    # Parse request
    req = request.get_json(silent=True)
    if req is None or (isinstance(req, dict) and not req):
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Missing required arguments.'
                }))
        return response, 400  # Bad Request
    if not req['meters']:
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Missing required arguments.'
                }))
        return response, 400  # Bad Request
    if not req['id']:
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Missing required arguments.'
                }))
        return response, 400  # Bad Request

    # Attempt to connect to the database.
    try:
        conn = db.connect_db()
    except Error as e:
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Could not create a connection to the database.',
                'Details': e
                }))
        return response, 500  # Internal Server Error
    check_meter_exists = 'SELECT COUNT(*) FROM meters WHERE meter_id = %s'
    check_id_type = 'SELECT entity_type FROM entities WHERE entity_id = %s'
    check_meter_status = 'SELECT COUNT(*) FROM meter_map WHERE meter_id = %s'
    check_user_meters = 'SELECT COUNT(*) FROM meter_map WHERE entity_id = %s'
    assign_meter = 'INSERT INTO meter_map (entity_id, meter_id) VALUES (%s, %s)'
    with conn.cursor() as cursor:
        cursor.execute(check_id_type, (req['id'],))
        result = cursor.fetchone()[0]
        if result == 'user':
            user_data, err = users.get_user_data(req['id'])
            if user_data['org_id']:
                response = make_response(
                    jsonify({
                        'ResponseType': 'Error',
                        'Message': 'Organization user cannot be assigned a meter'}))
                return response, 400  # Bad Request
            if len(req['meters']) > 1:
                response = make_response(
                    jsonify({
                        'ResponseType': 'Error',
                        'Message': 'User can only be assigned one meter'
                        }))
                return response, 400  # Bad Request
            cursor.execute(check_user_meters, (req['id'],))
            result = cursor.fetchone()[0]
            if result > 0:
                response = make_response(
                    jsonify({
                        'ResponseType': 'Error',
                        'Message': 'User is already associated with a meter'
                        }))
                return response, 400  # Bad Request
        for meter in req['meters']:
            cursor.execute(check_meter_exists, (meter,))
            result = cursor.fetchone()[0]
            if result == 0:
                response = make_response(
                    jsonify({
                        'ResponseType': 'Error',
                        'Message': 'Meters must be valid'
                        }))
                return response, 400  # Bad Request
            cursor.execute(check_meter_status, (meter,))
            result = cursor.fetchone()[0]
            if result > 1:
                response = make_response(
                    jsonify({
                        'ResponseType': 'Error',
                        'Message': 'Meter is already associated with an entity'
                        }))
                return response, 400  # Bad Request
            try:
                cursor.execute(assign_meter, (req['id'], meter))
            except Error as err:
                response = make_response(
                    jsonify({
                        'ResponseType': 'Error',
                        'Message': f'Unable to assign meter: {err}'
                        }))
                return response, 400  # Bad Request
        conn.commit()
        response = make_response(
            jsonify({
                'ResponseType': 'Success',
                'Message': 'Meters were assigned successfully'
                }))
        return response, 200  # OK

@meters.route('/unassigned', methods=['GET'])
def view_unassigned():
    """ Fetch All Unassigned Meters """
    # Fetch the session ID from the cookie.
    session_id = request.cookies.get('strSessionID')
    if session_id is None:
        # If the session ID is not provided, return an error.
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Session cookie does not exist.'
                }))
        return response, 400

    # Attempt to connect to the database.
    try:
        conn = db.connect_db()
    except Error as e:
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Could not create a connection to the database.',
                'Details': e
                }))
        return response, 500

    with conn.cursor(dictionary=True) as cursor:
        # Prepared sql statement gets account id and org id for provided session
        str_prep_sql = """
            SELECT sessions.account_id, users.org_id
            FROM sessions JOIN users on sessions.account_id = users.account_id
            WHERE sessions.session_id = %s;
            """
        cursor.execute(str_prep_sql, (session_id,))
        result = cursor.fetchone()
        # If there are no results we return an error
        if result is None:
            conn.close()
            response = make_response(
                jsonify({
                    'ResponseType': 'Error',
                    'Message': 'Unable to find session ID'
                    }))
            return response, 400

        # Response is in format [account_id, org_id]
        org_id = result['org_id']

        if org_id != 1:
            response = make_response(
                jsonify({
                    'ResponseType': 'Error',
                    'Message': 'Invalid permissions'
                    }))
            return response, 401

        str_prep_sql = """
            SELECT meter_id
            FROM (SELECT *, count(*) as count FROM meter_map GROUP BY meter_id) as S
            WHERE s.count <= 1;
            """
        cursor.execute(str_prep_sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        array = []
        for record in result:
            # Convert last updated time to relative time
            meter_object = { "meterID": record['meter_id'] }
            array.append(meter_object)

    response = make_response(
        jsonify({
            'ResponseType': 'Success',
            'Details': array
            }))
    return response, 200
