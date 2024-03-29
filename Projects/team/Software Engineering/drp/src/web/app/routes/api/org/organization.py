from flask import Blueprint, request, jsonify, make_response
from util.db import connect_db
from util.session import check_session
from mysql.connector import Error

organization = Blueprint('organization', __name__, url_prefix='/api/organization')

# -- Organization API Call --
# This call will return the organization name, email, first name, last name, approval status, and account ID of all users in the organization.
# The call will return the following JSON object:
# {
    # "ResponseType": "Success",
    # "Message": "Successfully retrieved organization members",
    # "Details": {
        # "org_name": "Organization Name",
        # "email": "Email",
        # "first_name": "First Name",
        # "last_name": "Last Name",
        # "approval_status": "Approval Status",
        # "account_id": "Account ID"
    # }
# }
# If there is an error, the call will return the following JSON object:
# {
#   "ResponseType": "Error",
#   "Message": "Error message here"
#   "Details": "Error details here"
# }
@organization.route("/", methods=['GET'])
# Lv0 org_id = 1 and approval_status = "Admin" -- shows all organizations and all their members
# Lv2 org_id != 1 (but every other) and approval_status = "Admin" -- shows my organization
def orgUserList():
    try:
        session_id = request.cookies.get('strSessionID')
        if session_id is None:
            response = make_response(jsonify({'ResponseType': 'Error', 'Message': 'Cookie does not contain a session ID.'}))
            return response, 400
    except Exception as err:
        response = make_response(jsonify({'ResponseType': 'Error', 'Message': 'Cookie is invalid', 'Details': str(err)}))
        return response, 400

    # Check the session ID
    status, err = check_session(session_id)

    if err:
        response = make_response(jsonify({'ResponseType': 'Error', 'Message': 'Unable to check session', 'Details': err}))
        return response, 500

    if not status:
        response.delete_cookie('strSessionID')
        response = make_response(jsonify({'ResponseType': 'Error', 'Message': 'Session is invalid'}))
        return response, 401

    # Connect to the database
    try:
        conn = connect_db()
    except Error as err:
        response = make_response(jsonify({'ResponseType': 'Error', 'Message': 'Could not create a connection to the database.', 'Details': str(err)}))
        return response, 500 
    
    results = None
    with conn.cursor() as cursor:
        # Check user level using session ID
        cursor.execute("""SELECT org_id, approval_status 
                    FROM users 
                    WHERE account_id = (SELECT account_id FROM sessions WHERE session_id = %s);""", (session_id,))
        verify_user = cursor.fetchall()
        
        # Process each row in verify_user
        for row in verify_user:
            org_id, approval_status = row
            if org_id == 1 and approval_status == "Admin": # LV 0 condition
                # Execute the query if the condition is met
                cursor.execute("""SELECT org_name, email, first_name, last_name, approval_status, account_id 
                       FROM users INNER JOIN organizations 
                       ON users.org_id = organizations.org_id;""")
                results = cursor.fetchall()
                break  # Break the loop as we found the matching user
            if org_id != 1 and approval_status == "Admin": # LV 2 condition
                # Execute the query if the condition is met
                cursor.execute("""SELECT org_name, email, first_name, last_name, approval_status, account_id 
                       FROM users INNER JOIN organizations 
                       ON users.org_id = organizations.org_id 
                       WHERE users.org_id = (SELECT org_id 
                       FROM users INNER JOIN sessions 
                       ON users.account_id = sessions.account_id WHERE session_id = %s)""", (session_id,))
                results = cursor.fetchall()
                break  # Break the loop as we found the matching user
            else:
                response = make_response(jsonify({'ResponseType': 'Error', 'Message': 'User does not have permission to view organization page'}))
                return response, 400

    # Close the connection outside the loop
    conn.close()
        
        # WHAT WAS THERE BEFORE USER PERMISSION STUFF
        # cursor.execute("""SELECT org_name, email, first_name, last_name, approval_status, account_id 
        #                FROM users INNER JOIN organizations 
        #                ON users.org_id = organizations.org_id 
        #                WHERE users.org_id = (SELECT org_id 
        #                FROM users INNER JOIN sessions 
        #                ON users.account_id = sessions.account_id WHERE session_id = %s)""", (session_id,))
        # results = cursor.fetchall()
        # conn.close()
    if results is None:
        response = make_response(jsonify({'ResponseType': 'Error', 'Message': 'User is not associated with organization'}))
        return response, 400

    # Return a JSON object as `results`.
    response = make_response(jsonify({'ResponseType': 'Success', 'Message': 'Successfully retrieved organization members', 'usersArray': results, 'strOrgName' : results[0][0] }))
    return response, 200

@organization.route("/", methods=['PUT'])
def orgModUsers():
    data = request.json  # sending JSON data

    intModUserID = data.get('intModUserID')

    strOldEmail = data.get('strOldEmail')
    strNewEmail = data.get('strNewEmail')

    strOldFirst = data.get('strOldFirst')
    strNewFirst = data.get('strNewFirst')

    strOldLast = data.get('strOldLast')
    strNewLast = data.get('strNewLast')

    strOldStatus = data.get('strOldStatus')
    strNewStatus = data.get('strNewStatus')

    # Connect to the database
    try:
        conn = connect_db()
    except Error as err:
        response = make_response(jsonify({'ResponseType': 'Error', 'Message': 'Could not create a connection to the database.', 'Details': str(err)}))
        return response, 500

    with conn.cursor() as cursor:
        if len(strNewEmail) > 0 and strNewEmail != strOldEmail:
            cursor.execute('UPDATE users SET email = %s where account_id = %s', (strNewEmail, intModUserID))
            conn.commit()

        if len(strNewFirst) > 0 and strNewFirst != strOldFirst:
            cursor.execute('UPDATE users SET first_name = %s where account_id = %s', (strNewFirst, intModUserID))
            conn.commit()

        if len(strNewLast) > 0 and strNewLast != strOldLast:
            cursor.execute('UPDATE users SET last_name = %s where account_id = %s', (strNewLast, intModUserID))
            conn.commit()

        if strNewStatus != strOldStatus:
            cursor.execute('UPDATE users SET approval_status = %s where account_id = %s', (strNewStatus, intModUserID))
            conn.commit()

    conn.close()
    response = make_response(jsonify({'ResponseType': 'Success', 'Message': 'Successfully updated user'}))
    return response, 201
