# --- PROJECT ---
# 2023 CSC 4610-4620
# Demand Response Portal
# Evyn Price, Serena Labelle, Elijah Monroe, Mykola (Nick) Omelchenko,
# Shelby Smith, William Goodson, Won (Brian) Lee

""" Flask API Server Entry Point """
# Imports
import os
from flask import Flask, request, abort
from flask_cors import CORS
from util.db import start_redis_check, REDIS_AVAILABLE

from routes.api.vis.bokeh import bokeh
from routes.api.user.user import user
from routes.api.org.organization import organization
from routes.api.user.session import session as route_session
from routes.api.account.pass_reset import passwordReset
from routes.api.entity.meters import meters
from routes.api.vis.data import vis_data
from routes.api.admin.adminpage import adminpage

start_redis_check(REDIS_AVAILABLE)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://$host$request_uri"}})

@app.before_request
def check_sec_fetch_site():
    """ Checks Request To Ensure Same Origin """
    sec_fetch_site = request.headers.get('sec-fetch-site')

    if sec_fetch_site not in ('same-origin', 'same-site'):
        abort(403)

app.register_blueprint(bokeh)
app.register_blueprint(organization)
app.register_blueprint(user)
app.register_blueprint(route_session)
app.register_blueprint(passwordReset)
app.register_blueprint(meters)
app.register_blueprint(vis_data)
app.register_blueprint(adminpage)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
