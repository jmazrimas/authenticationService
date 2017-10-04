from flask import request, current_app, Blueprint, render_template, make_response, jsonify
from database import db_session
from models import User
import requests
import google_auth
from datetime import datetime
import user_controller

authentication = Blueprint('authentication', __name__)

@authentication.route("/")
def main():
    data = {'testJsonKey': 'testJsonValue NEW'}
    response = make_response(jsonify(data))
    response.set_cookie('dmc_session', 'SESSIONHASHx')
    return response

@authentication.route("/login")
def login():

    return render_template('login.html', login_url=google_auth.login_url)

@authentication.route("/login-callback")
def login_callback():
    code = request.args.get('code')
    user_info = google_auth.get_user_keys(code)
    session_hash = user_controller.get_or_create_google(user_info)

    response = make_response(
        render_template(
        'login-callback.html',
        user_name=user_info['name'],
        user_id=user_info['user_id'])
    )

    response.set_cookie('dmc_session', session_hash)
    return response


@authentication.route("/validate-user")
def validate_user():
    if 'dmc_session' in request.cookies:
        print 'public USER', user_controller.return_valid_user(request.cookies.get('dmc_session'))
    data = {'testJsonKey': 'testJsonValue NEW'}
    response = make_response(jsonify(data))
    return response