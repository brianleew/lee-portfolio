""" Route For Handling Password Resets """

import bcrypt
from flask import Blueprint, request, jsonify
from mysql.connector import Error

from util import db

passwordReset = Blueprint('passwordReset', __name__, url_prefix='/api/passwordReset')

# --Password Reset--
# Allows user change password based on Meter ID/Oranization ID and email.

@passwordReset.route("/", methods=['POST'])
def password_reset_call():
    """ Resets User Password """
    req = request.get_json(silent=True)
    if req is None or req is {}:
        return jsonify({'Error': 'Empty Request'}), 400
    # # Get user input of meter ID/Account ID, email, and new password.
    # if(intID is None and request.args.getlist('intID') is not None):
    #     intID = request.args.getlist('intID')[0]

    # if(strEmail is None and request.args.getlist('strEmail') is not None):
    #     strEmail = request.args.getlist('strEmail')[0]

    # if(strNewPassword is None and request.args.getlist('strNewPassword') is not None):
    #     strNewPassword = request.args.getlist('strNewPassword')[0]

    # request.


    # Hash new Password
    byte_salt = bcrypt.gensalt()
    byte_hashed_password = bcrypt.hashpw(req['strNewPassword'].encode('utf-8'), byte_salt)
    print(byte_hashed_password)


    # 2 sql quieries 1 for MeterId or 1 for AccountID
    try:
        conn = db.connect_db()
    except Error as e:
        return jsonify({"Error":"Server couldn't connect to the database", "Details": e})

    # Quiery the database to get email and meterID related to the accountID
    with conn.cursor(dictionary=True) as cursor:
        str_prep_sql = "SELECT account_id, org_id from users where email = %s;"
        cursor.execute(str_prep_sql, (req['strEmail'],))
        results = cursor.fetchone()

        if results is None:
            conn.close()
            return jsonify({"Error":"No account found for provided email."})
        account_id = results['account_id']
        int_id = int(req['intID'])
        ## IF user has org id and intID is not equal to that org_id fail
        if results['org_id'] is not None and results['org_id'] != int_id:
            return jsonify({"Error":"Not authenticated"})
        ## if intID is their org_id then ##
        if results['org_id'] == int_id:
            update_sql = "UPDATE logins SET password_hash = %s WHERE account_id = %s"
            try:
                cursor.execute(update_sql, (byte_hashed_password, account_id))
                conn.commit()

                # Check if results are valid and send a response
                return jsonify({"Success":"Entered data matched the database"})
            except Error as e:
                return jsonify({"Error":"Could not update password", "Details": e})
        ## if user does not have org_id then try residential ##
        if results['org_id'] is None:
            # step 2, if there is no organization_id, check the user against meter map.
            str_prep_sql = """
                SELECT account_id
                FROM users JOIN meter_map ON users.account_id = meter_map.entity_id
                WHERE email = %s and meter_id = %s
                """
            cursor.execute(str_prep_sql, (req['strEmail'], int_id))
            results = cursor.fetchone()
            # if no results
            if len(results) == 0:
                return jsonify(
                    {"Error":"Meter ID or email is/are not found. Please try again."}
                )
            # Meter ID and Email match the database records
            # Insert new password in the database
            update_sql = "UPDATE logins SET password_hash = %s WHERE account_id = %s"
            try:
                cursor.execute(update_sql, (byte_hashed_password, int(results['account_id'])))
                conn.commit()
                return jsonify({"Success":"Entered data matched the database"})
            except Error as e:
                return jsonify(
                    {"Error": "(Users) Could not update password", "Details": e}
                ), 400