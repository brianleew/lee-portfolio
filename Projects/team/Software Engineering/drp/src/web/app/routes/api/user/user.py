""" Route For Handling Users """

import bcrypt
from flask import Blueprint, jsonify, request, make_response
from mysql.connector import Error

from util import db
from util.session import get_session_data
from util.users import get_user_data, update_user_data, delete_user_data

user = Blueprint('user', __name__, url_prefix='/api/user')

# -- View User API Call --
# This call will view the user data, it will take the following arguments:
# strSessionID: The session ID of the user
# The call will return the following JSON object:
# {
    # "ResponseType": "Success",
    # "Message": "Successfully retrieved user data",
    # "Details": {
        # "account_id": 1,
        # "email": "test@test",
        # "first_name": "test",
        # "last_name": "test",
        # "org_id": 1
    # }
# }
# If there is an error, the call will return the following JSON object:
# {
    # "ResponseType": "Error",
    # "Message": "Error message here"
    # "Details": "Error details here"
# }
@user.route('/', methods=['GET'])
def view_user():
    """ Fetch User Data """
    # Get the session ID from the cookie.
    session_id = request.cookies.get('strSessionID')
    if session_id is None:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Cookie does not contain a session ID.'
            }))
        return response, 400

    # Check the session ID
    session_data, err = get_session_data(session_id)
    if err:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Unable to check session',
            'Details': err
            }))
        return response, 500

    # Get the user data
    account_id = session_data['account_id']
    user_data, err = get_user_data(account_id)
    if err:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Unable to get user',
            'Details': err
            }))
        return response, 500

    response = make_response(jsonify({
        'ResponseType': 'Success',
        'Message': 'Successfully retrieved user data',
        'Details': user_data
        }))
    return response, 200

# -- Update User API Call --
# This call will update the user data, it will take the following arguments:
# strSessionID: The session ID of the user
# str_firstname: The first name of the user
# str_lastname: The last name of the user
# str_email: The email of the user
# The call will return the following JSON object:
# {
    # "ResponseType": "Success",
    # "Message": "Successfully updated user"
# }
# If there is an error, the call will return the following JSON object:
# {
    # "ResponseType": "Error",
    # "Message": "Error message here"
    # "Details": "Error details here"
# }
@user.route('/update', methods=['PATCH'])
def update_user():
    """ Update User Data """
    req = request.get_json(silent=True)
    if req is None or req is {}:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Missing required arguments.'
            }))
        return response, 400

    session_id = request.cookies.get('strSessionID')
    if session_id is None:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Cookie does not contain a session ID.'
            }))
        return response, 400

    # Get session data
    session_data, err = get_session_data(session_id)
    if err:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Unable to check session',
            'Details': err
            }))
        return response, 500

    # Get the user data
    account_id = session_data['account_id']
    status, err = update_user_data(account_id, req)
    if err:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Unable to get user',
            'Details': err
            }))
        return response, 500

    if status:
        response = make_response(jsonify({
            'ResponseType': 'Success',
            'Message': 'Successfully updated user'
            }))
        return response, 201

## DELETE USER DATA ##
@user.route('/delete', methods=['DELETE'])
def delete():
    """ Delete User Data """
    # Get the session ID from the cookie.
    session_id = request.cookies.get('strSessionID')
    if session_id is None:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Cookie does not contain a session ID.'
            }))
        return response, 400

    # Check the session ID
    session_data, err = get_session_data(session_id)
    if err:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Unable to check session',
            'Details': err
            }))
        return response, 500

    # Get the user data
    account_id = session_data['account_id']
    user_data, err = delete_user_data(account_id)
    if err:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Unable to delete user',
            'Details': err
            }))
        return response, 500

    response = make_response(jsonify({
        'ResponseType': 'Success',
        'Message': 'Successfully deleted user data',
        'Details': user_data
        }))
    return response, 201

# --- Register User API Call ---
# This call will register a new user into the database, it will take the following arguments:
# str_email: The email of the user
# str_password: The password of the user
# str_firstname: The first name of the user
# str_lastname: The last name of the user
# int_id: The organization or meter ID that the user is assigned to
# After creating a new user, it will also create a new login entry for the user and add the user's
# account ID in the meter_map table, if applicable.
#
# The call will return the following JSON object:
# {
    # "ResponseType": "Success",
    # "Message": "Successfully created new user."
# }

# If there is an error, the call will return the following JSON object:
# {
    # "ResponseType": "Error",
    # "Message": "Error message here"
    # "Details": "Error details here"
# }
@user.route('/register', methods=['POST'])
def register_user_call():
    """ Create User Data """
    # Get the arguments from the request.
    str_email = request.form.get('strEmail')
    str_password = request.form.get('strPassword')
    str_firstname = request.form.get('strFirstName')
    str_lastname = request.form.get('strLastName')
    if request.form.get('intID') is not None:
        int_id = int(request.form.get('intID'))
    else:
        int_id = None

    # Check that all arguments are present.
    if (
        str_email is None or
        str_password is None or
        str_firstname is None or
        str_lastname is None or
        int_id is None
        ):
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Missing required arguments.'
            }))
        return response, 400

    # Attempt to connect to the database.
    try:
        conn = db.connect_db()
    except Error as err:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Could not create a connection to the database.',
            'Details': str(err)
            }))
        return response, 500

    with conn.cursor(dictionary=True) as cursor:
        # Check that the email is not already in use
        str_prep_sql = 'SELECT * from users WHERE email = %s'
        cursor.execute(str_prep_sql, (str_email,))
        results = cursor.fetchall()
        if(results is not None and len(results) > 0):
            conn.close()
            response = make_response(jsonify({
                'ResponseType': 'Error',
                'Message': 'Unable to create a user with an email that is already in use.'
                }))
            return response, 400

        # Check if organization ID exists in database.
        is_org = False
        str_prep_sql = 'SELECT * from organizations WHERE org_id = %s'
        cursor.execute(str_prep_sql, (int_id,))
        results = cursor.fetchall()
        if(results is not None and len(results) > 0):
            is_org = True

        if not is_org:
            # Check if meter ID exists in database.
            str_prep_sql = 'SELECT * from meters WHERE meter_id = %s'
            cursor.execute(str_prep_sql, (int_id,))
            results = cursor.fetchall()
            if(results is None or len(results) == 0):
                conn.close()
                response = make_response(jsonify({
                    'ResponseType': 'Error',
                    'Message': 'Unable to create a user with an invalid organization or meter ID.'
                    }))
                return response, 400

        # If the organization ID is valid, create a new user.
        if is_org:
            try:
                str_prep_sql = """
                    INSERT INTO users (email, first_name, last_name, org_id)
                    VALUES( %s, %s, %s, %s);
                    """
                cursor.execute(str_prep_sql, (str_email, str_firstname, str_lastname, int_id))
            except Error as err:
                # If there is an error, return an error.
                conn.close()
                response = make_response(jsonify({
                    'ResponseType': 'Error',
                    'Message': 'Could not insert user into users table.',
                    'Details': str(err)
                    }))
                return response, 500
        else:
            # Check if the meter is already assigned to a user.
            str_prep_sql = 'SELECT * from meters NATURAL JOIN meter_map WHERE meter_id = %s'
            cursor.execute(str_prep_sql, (int_id,))
            results = cursor.fetchall()

            # If the meter is already assigned to a user, return an error.
            if(results is not None and len(results) > 0):
                response = make_response(jsonify({
                    'ResponseType': 'Error',
                    'Message': 'Unable to assign a meter that is already assigned'
                    }))
                return response, 400

            # If the meter ID is valid, create a new user.
            try:
                str_prep_sql = """
                    INSERT INTO users (email, first_name, last_name)
                    VALUES( %s, %s, %s)
                    """
                cursor.execute(str_prep_sql, (str_email, str_firstname, str_lastname))
            except Error as err:
                # If there is an error, return an error.
                conn.close()
                response = make_response(jsonify({
                    'ResponseType': 'Error',
                    'Message': 'Could not insert user into users table.',
                    'Details': str(err)
                    }))
                return response, 500

        # Fetch the account ID of the newly created user.
        str_prep_sql = 'SELECT account_id from users where email = %s'
        cursor.execute(str_prep_sql, (str_email,))
        results = cursor.fetchone()
        int_account_id = int(results['account_id'])

        if not is_org:
            # Create a new entry in the meter_map table for the user.
            try:
                str_prep_sql = 'INSERT INTO meter_map (entity_id, meter_id) VALUES(%s, %s)'
                cursor.execute(str_prep_sql, (int_account_id, int_id))
            except Error as err:
                conn.close()
                response = make_response(jsonify({
                    'ResponseType': 'Error',
                    'Message': 'Could not insert user into meter_map table.',
                    'Details': str(err)
                    }))
                return response, 500

        # Create a new login entry for the user.
        byte_salt = bcrypt.gensalt()
        byte_hashed_password = bcrypt.hashpw(bytes(str_password, 'utf-8'), byte_salt)

        try:
            str_prep_sql = 'INSERT INTO logins (account_id, password_hash) VALUES (%s, %s)'
            cursor.execute(str_prep_sql, (int_account_id, byte_hashed_password))
            conn.commit()
        except Error as err:
            conn.close()
            response = make_response(jsonify({
                'ResponseType': 'Error',
                'Message': 'Could not insert user into logins table.',
                'Details': str(err)
                }))
            return response, 500

        # Close the connection to the database and return a success message.
        conn.close()
        response = make_response(jsonify({
            'ResponseType': 'Success',
            'Message': 'Successfully created new user.'
            }))
        return response, 201

@user.route('/permissions', methods=['GET'])
def get_permissions():
    """ Fetch Users Permissions """
    # Get the user's session ID
    session_id = request.cookies.get('strSessionID')
    if session_id is None:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Cookie does not contain a session ID.'
            }))
        return response, 400

    # Check the session ID
    session_data, err = get_session_data(session_id)
    if err:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Unable to check session',
            'Details': err
            }))
        return response, 500

    # Get the user data
    account_id = session_data['account_id']
    results, err = get_user_data(account_id)

    if err:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Unable to find user'
            }))
        return response, 400

    # If user is an admin of the distributor organization, permission level 0
    if results['org_id'] == 1 and results['approval_status'] == 'Admin':
        response = make_response(jsonify({
            'ResponseType': 'Success',
            'Message': 'Successfully retrieved permissions',
            'Level': 0
            }))
        return response, 200

    # If the user is a member of the distributor organization, permission level 1
    if results['org_id'] == 1 and results['approval_status'] != 'Pending':
        response = make_response(jsonify({
            'ResponseType': 'Success',
            'Message': 'Successfully retrieved permissions',
            'Level': 1
            }))
        return response, 200

    # If the user is an admin of an organization, permission level 2
    if results['org_id'] is not None and results['approval_status'] == 'Admin':
        response = make_response(jsonify({
            'ResponseType': 'Success',
            'Message': 'Successfully retrieved permissions',
            'Level': 2
            }))
        return response, 200

    # If the user is a member of an organization, permission level 3
    if results['org_id'] is not None and results['approval_status'] != 'Pending':
        response = make_response(jsonify({
            'ResponseType': 'Success',
            'Message': 'Successfully retrieved permissions',
            'Level': 3
            }))
        return response, 200

    # If the user has a meter assigned to them, permission level 4
    if results['org_id'] is None:
        response = make_response(jsonify({
            'ResponseType': 'Success',
            'Message': 'Successfully retrieved permissions',
            'Level': 4
            }))
        return response, 200

    # If the user is pending or has no permissions, permission level 5
    response = make_response(jsonify({
        'ResponseType': 'Success',
        'Message': 'Successfully retrieved permissions',
        'Level': 5
        }))
    return response, 200
