import html
from flask import Blueprint, jsonify, request, make_response
from util.vis import test_bokeh_json_dumps, get_meter_data,get_pie_data,get_total_data,get_acf_data,get_pacf_data,get_sig_data

# Create a Blueprint for Bokeh-related API endpoints
bokeh = Blueprint('bokeh', __name__, url_prefix='/api/vis/')


# --- Get Bokeh Meter API Call ---
# This call send a meter-id to the bokehMeter function that returns a JSON dump, which will be sent back to the html
#

# The html.escape function is part of the html module and is the correct way to escape characters that have special meaning in HTML
@bokeh.route('/', methods=['GET'])
def view():
    # Retrieve the session ID from a cookie
    session_id = request.cookies.get('strSessionID')
    # Sanitize and escape the session ID to prevent Cross-Site Scripting (XSS) attacks
    sanitized_session_id = html.escape(session_id)
    # Call 'test_bokeh_json_dumps' to generate the response
    return test_bokeh_json_dumps(sanitized_session_id)

@bokeh.route('/meter_data/<int:meter_id>/', methods=['GET'])
def meter_data(meter_id):
    session_id = request.cookies.get('strSessionID')
    sanitized_session_id = html.escape(session_id)  
    return get_meter_data(sanitized_session_id, meter_id)

@bokeh.route('/pie_data/<int:meter_id>/', methods=['GET'])
def pie_data(meter_id):
    session_id = request.cookies.get('strSessionID')
    sanitized_session_id = html.escape(session_id) 
    return get_pie_data(sanitized_session_id, meter_id)

@bokeh.route('/total_data/<int:meter_id>/', methods=['GET'])
def total_data(meter_id):
    session_id = request.cookies.get('strSessionID')
    sanitized_session_id = html.escape(session_id) 
    return get_total_data(sanitized_session_id, meter_id)

@bokeh.route('/acf_data/<int:meter_id>/', methods=['GET'])
def acf_data(meter_id):
    session_id = request.cookies.get('strSessionID')
    sanitized_session_id = html.escape(session_id) 
    return get_acf_data(sanitized_session_id, meter_id)

@bokeh.route('/pacf_data/<int:meter_id>/', methods=['GET'])
def pacf_data(meter_id):
    session_id = request.cookies.get('strSessionID')
    sanitized_session_id = html.escape(session_id) 
    return get_pacf_data(sanitized_session_id, meter_id)

@bokeh.route('/sig_data/<int:meter_id>/', methods=['GET'])
def sig_data(meter_id):
    session_id = request.cookies.get('strSessionID')
    sanitized_session_id = html.escape(session_id) 
    return get_sig_data(sanitized_session_id, meter_id)
