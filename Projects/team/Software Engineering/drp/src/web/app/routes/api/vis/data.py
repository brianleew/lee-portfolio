""" Fetch Meter Data For Visualizations """

from datetime import timedelta
from flask import Blueprint, request, jsonify, make_response
import numpy as np
from mysql.connector import Error
from util import users, session, db

vis_data = Blueprint('vis_data', __name__, url_prefix='/api/vis/data')

# REQUEST JSON { 'meter_id': <meter_id> }
# RESPONSE JSON { ResponseType: '', Message: '', Data: { real: [...], prediction: [...] } }


@vis_data.route('/', methods=['POST'])
def get_meter_data():
    """ Fetch Meter Data Available To Specified User """
    # Check Session ID Exists
    session_id = request.cookies.get('strSessionID')
    if session_id is None:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Cookie does not contain a session ID.'
            }))
        return response, 400
    # Parse Request
    req = request.get_json(silent=True)
    if req is None or (isinstance(req, dict) and not req):
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Missing required arguments.'
            }))
        return response, 400
    if 'meter_id' not in req:
        response = make_response(jsonify({
            'ResponseType': 'Error',
            'Message': 'Missing required arguments.'
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
        return response, 500  # Internal Server Error
    fetch_meter_data = """
        SELECT meter_value, prediction_value, start_time
        FROM meter_data
        WHERE meter_id = %s;
        """
    # FUTURE SPACE FOR CHECKING CACHE FOR CONNECTION IN DB=1
    session_data, err = session.get_session_data(session_id)
    if err is not None:
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Could not fetch session data',
                'Details': err
                }))
        return response, 500  # Internal Server Error
    status, err = users.can_access_meter(
        session_data['account_id'],
        req['meter_id'])
    if not status:
        response = make_response(
            jsonify({
                'ResponseType': 'Error',
                'Message': 'Unable to verify permissions',
                'Details': err
                }))
        return response, 401

    # FUTURE SPACE FOR CHECKING CACHE FOR METER DATA IN DB=2
    with conn.cursor(dictionary=True) as cursor:
        # Fetch Data
        cursor.execute(fetch_meter_data, (req['meter_id'],))
        data = cursor.fetchall()
        if not data:
            response = make_response(
                jsonify({
                    'ResponseType': 'Error',
                    'Message': 'Meter has no data'
                    }))
            return response, 400  # Bad Request
    # Format Data
    #   Get start_date
    start_date = data[0]['start_time']
    #   Get end_date
    end_data = data[len(data)-1]['start_time']
    #   Set step
    step = timedelta(minutes=30)
    #   Create date range
    date_range = np.arange(start_date, end_data, step)
    #   Init arrays
    real = [None] * len(date_range)
    prediction = [None] * len(date_range)
    #   populate arrays
    for entry in data:
        index = int((entry['start_time'] - start_date) / step)
        if index < len(date_range):
            if entry['meter_value'] is None:
                real[index] = entry['meter_value']
            else:
                real[index] = float(entry['meter_value'])
            if entry['prediction_value'] is None:
                prediction[index] = entry['prediction_value']
            else:
                prediction[index] = float(entry['prediction_value'])
    # Return Data
    response = make_response(
        jsonify({
            'ResponseType': 'Success',
            'Message': 'Successfully retrieved meter data',
            'Data': {'real': real, 'prediction': prediction}
            })
    )
    # FUTURE SPACE FOR CACHING METER DATA IN DB=2
    return response, 200
