""" Route For Handling Sessions """
from flask import Blueprint, jsonify, request, make_response
from bcrypt import checkpw
from util.db import connect_db
from util.session import grant_session, check_session, revoke_session
from mysql.connector import Error

session = Blueprint('session', __name__, url_prefix='/api/user/session')

# -- Validate Session API Call --
# This call will validate a session ID, it will take the following arguments:
# strSessionID: The session ID to validate
# The call will return the following JSON object:
# {
    # "ResponseType": "Success",
    # "Message": "Session is valid"
# }
# If there is an error, the call will return the following JSON object:
# {
    # "ResponseType": "Error",
    # "Message": "Error message here"
    # "Details": "Error details here"
# }
@session.route('/validate', methods=['GET'])
def validate_session ():
    """ Checks Validity Of Session """
    # Get the session ID from the cookie.
    session_id = request.cookies.get('strSessionID')
    if session_id is None:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Cookie does not contain a session ID.'
            }))
        return response, 400

    # Check the session ID
    status, err = check_session(session_id)

    if err:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Unable to check session',
            'Details': err
            }))
        return response, 401

    # If the session is invalid, delete the cookie and return an error.
    if not status:
        response.delete_cookie('strSessionID')
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Session is invalid'
            }))
        return response, 401

    # Return a valid status
    response = make_response(jsonify({
        'ResponseType': 'Success',
        'Message': 'Session is valid'
        }))
    return response, 200

# -- Create Session API Call --
# This call will create a new session ID, it will take the following arguments:
# str_email: The email of the user
# str_password: The password of the user
# The call will return the following JSON object:
# {
    # "ResponseType": "Success",
    # "Message": "Successfully created new session",
    # "Details": {
        # "sessionID": "session_id"
    # }
# }
# If there is an error, the call will return the following JSON object:
# {
    # "ResponseType": "Error",
    # "Message": "Error message here"
    # "Details": "Error details here"
# }
@session.route('/create', methods=['POST'])
def create_session ():
    """ Creates User Session """
    # Get the arguments from the request.
    str_email = request.form.get('strEmail')
    str_password = request.form.get('strPassword')
    # Check that all arguments are present.
    if str_email is None or str_password is None:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Missing required arguments.'
            }))
        return response, 400

    # Connect to the database
    try:
        conn = connect_db()
    except Error as err:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Could not create a connection to the database.',
            'Details': str(err)
            }))
        return response, 500

    # Query the database for the user
    with conn.cursor(dictionary=True) as cursor:
        try:
            str_prep_sql = """
                SELECT l.account_id, l.password_hash
                FROM users as u JOIN logins as l ON u.account_id = l.account_id
                WHERE u.email = %s;
                """
            cursor.execute(str_prep_sql, (str_email,))
            result = cursor.fetchone()
            conn.close()
        except Error as err:
            conn.close()
            response = make_response(jsonify({
                'ResponseType': 'Error',
                'Message': 'Unable to query database',
                'Details': str(err)
                }))
            return response, 500

    # If the user does not exist or password is incorrect, return an error
    valid_password = checkpw(str_password.encode('utf-8'), result['password_hash'].encode('utf-8'))
    if result is None or result == {} or not valid_password:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Invalid email or password'
            }))
        return response, 401

    # Grant a new session
    session_id, err = grant_session(result['account_id'])
    if err:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Unable to grant session',
            'Details': err
            }))
        return response, 500

    response = make_response(jsonify({
        'ResponseType': 'Success',
        'Message': 'Successfully created new session',
        'Details': {'sessionID': session_id}
        }))
    response.set_cookie('strSessionID', session_id)
    return response, 200

# -- Delete Session API Call --
# This call will delete a session ID, it will take the following arguments:
# strSessionID: The session ID to delete
# The call will return the following JSON object:
# {
    # "ResponseType": "Success",
    # "Message": "Session deleted successfully"
# }
# If there is an error, the call will return the following JSON object:
# {
    # "ResponseType": "Error",
    # "Message": "Error message here"
    # "Details": "Error details here"
# }
@session.route('/delete', methods=['DELETE'])
def delete_session ():
    """ Deletes User Session """
    # Get the session ID from the cookie.
    session_id = request.cookies.get('strSessionID')
    if session_id is None:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Cookie does not contain a session ID.'
            }))
        return response, 400

    # Call the revoke session function
    status, err = revoke_session(session_id)
    if not status:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Unable to revoke session',
            'Details': err
            }))
        return response, 500

    # Delete the cookie and return a success
    response = make_response(jsonify({
        'ResponseType': 'Success',
        'Message': 'Session deleted successfully'
        }))
    response.delete_cookie('strSessionID')
    return response, 200
