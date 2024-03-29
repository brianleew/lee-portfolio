from flask import Blueprint, request, jsonify, make_response
from util.db import connect_db
from util.session import check_session
from mysql.connector import Error

adminpage = Blueprint('adminpage', __name__, url_prefix='/api/adminpage')

@adminpage.route("/", methods=['GET'])
def orgList(): # function to get all of the orgs and its members and meters
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
        with conn.cursor() as cursor:
            # query unique org_id and its org_name, number of unique members per unique org_id, and number of unique meters per unique org_id
            cursor.execute("""
                            SELECT A.org_id, A.org_name, COALESCE(B.org_member_count, 0) AS org_member_count, COALESCE(C.meter_count, 0) AS meter_count
                            FROM organizations AS A
                            LEFT JOIN (
                                SELECT org_id, COUNT(*) AS org_member_count
                                FROM users
                                GROUP BY org_id
                            ) AS B ON A.org_id = B.org_id
                            LEFT JOIN (
                                SELECT entity_id AS org_id, COUNT(*) AS meter_count
                                FROM meter_map
                                GROUP BY entity_id
                            ) AS C ON A.org_id = C.org_id;
                            """)
            results = cursor.fetchall()
            # return a JSON object containing unique org_id and its org_name, number of unique members per unique org_id, and number of unique meters per unique org_id as `results`.
            return make_response(jsonify({'ResponseType': 'Success', 'Message': 'Successfully retrieved all of the organization ids and its names', 'orgsArray': results }))
    except Error as err:
        return make_response(jsonify({'ResponseType': 'Error', 'Message': 'Database error', 'Details': str(err)})), 500
    finally:
        if conn:
            conn.close()

@adminpage.route("/mod-org-name", methods=['PUT'])
def modOrgName(): # button to mod an org name
    # ajax request to get unique org_id and its org_name and new org_name
    data = request.json
    intOrgNum = data.get('intOrgNum')
    strNewOrgName = data.get('strNewOrgName')
    strCurrOrgName = data.get('strCurrOrgName')
    
    # Connect to the database
    try:
        conn = connect_db()
        # Update the database if organization name is changed
        with conn.cursor() as cursor:
            if len(strNewOrgName) > 0 and strNewOrgName != strCurrOrgName:
                cursor.execute('UPDATE organizations SET org_name = %s where org_id = %s', (strNewOrgName, intOrgNum))
                conn.commit()
                return make_response(jsonify({'ResponseType': 'Success', 'Message': 'Successfully updated organization name'})), 201
            else:
                return make_response(jsonify({'ResponseType': 'Error', 'Message': 'Conditions not met'})), 400
    except Error as err:
        return make_response(jsonify({'ResponseType': 'Error', 'Message': 'Database error', 'Details': str(err)})), 500
    finally:
        if conn:
            conn.close()

@adminpage.route("/add-meter-to-org", methods=['PUT'])
def addMeterToOrg(): # button to add a meter to an org
    # ajax request to get unique org_id and new meter_id adding to the org
    data = request.json
    intOrgNum = data.get('intOrgNum')
    intMeterID = data.get('intMeterID')
    
    # Connect to the database
    try:
        conn = connect_db()
        with conn.cursor() as cursor:
            
            # Check if the intMeterID is assigned to an org_id aka entity_id (except the default entity_id or org_id = 1)
            cursor.execute("SELECT * FROM meter_map WHERE meter_id=%s and not entity_id = 1", (intMeterID,))
            result = cursor.fetchall()

            # If the 'wanting to change' meter_id is not assigned to an org_id, then add it to the 'wanting to add' org_id
            if not result and len(intMeterID) > 0: # also check if user input meter_id is not empty
                cursor.execute('INSERT INTO meter_map (entity_id, meter_id) VALUES (%s, %s)', (intOrgNum, intMeterID))
                conn.commit()
                return make_response(jsonify({'ResponseType': 'Success', 'Message': 'Successfully added meter to an organization'})), 201
            else:
                return make_response(jsonify({'ResponseType': 'Error', 'Message': 'Conditions not met'})), 400
    except Error as err:
        return make_response(jsonify({'ResponseType': 'Error', 'Message': 'Database error', 'Details': str(err)})), 500
    finally:
        if conn:
            conn.close()
            
@adminpage.route("/create-new-org", methods=['PUT'])
def createNewOrg(): # button to create an org
    # ajax call to get the 'wanting to add' org_name
    data = request.json
    strOrgName = data.get('strOrgName')
    
    try:
        conn = connect_db() # connect to the database
        with conn.cursor() as cursor:
            # query to check if the 'wanting to add' org_name already exists in the 'organizations' table
            cursor.execute("SELECT EXISTS(SELECT 1 FROM organizations WHERE org_name=%s LIMIT 1)", (strOrgName,))
            exists_in_orgs = cursor.fetchone()[0]
            if exists_in_orgs:
                return make_response(jsonify({'ResponseType': 'Error', 'Message': 'Organization already exists'})), 400
            else: # if 'wanting to add' org_name does not exist in the 'organizations' table, then add it
                cursor.execute('INSERT INTO organizations (org_name) VALUES (%s)', (strOrgName,))
                conn.commit()
                return make_response(jsonify({'ResponseType': 'Success', 'Message': 'Successfully created an organization'})), 201
    except Error as err:
        return make_response(jsonify({'ResponseType': 'Error', 'Message': 'Database error', 'Details': str(err)})), 500
    finally:
        if conn:
            conn.close()

@adminpage.route("/create-new-meter", methods=['PUT'])     
def createNewMeter(): # button to create a meter
    # ajax call to get the 'wanting to add' meter_id
    data = request.json
    strMeterID = data.get('strMeterID')
    
    try:
        conn = connect_db() # connect to the database
        with conn.cursor() as cursor:
            # query to check if the 'wanting to add' meter_id already exists in the 'meters' table
            cursor.execute("SELECT EXISTS(SELECT 1 FROM meters WHERE meter_id=%s LIMIT 1)", (strMeterID,))
            exists_in_meters = cursor.fetchone()[0]
            if exists_in_meters:
                return make_response(jsonify({'ResponseType': 'Error', 'Message': 'Meter already exists'})), 400
            else: # if 'wanting to add' meter_id does not exist in the 'meters' table, then add it
                cursor.execute('INSERT INTO meters (meter_id) VALUES (%s)', (strMeterID,))
                conn.commit()
                return make_response(jsonify({'ResponseType': 'Success', 'Message': 'Successfully created a meter'})), 201
    except Error as err:
        return make_response(jsonify({'ResponseType': 'Error', 'Message': 'Database error', 'Details': str(err)})), 500
    finally:
        if conn:
            conn.close()


