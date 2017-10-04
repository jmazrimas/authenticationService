from flask import request, current_app, Blueprint, render_template
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
    response.set_cookie('username', 'the username')
    return response

@authentication.route("/login")
def login():

    return render_template('login.html', login_url=google_auth.login_url)

@authentication.route("/login-callback")
def login_callback():
    code = request.args.get('code')
    token_url = google_auth.generate_token_url(code)
    res = requests.post(token_url)
    access_token = res.json()['access_token']
    expires_in = res.json()['expires_in']
    refresh_token = res.json()['refresh_token']

    user_info = google_auth.get_user_info(access_token)

    user_controller.get_or_create_google(user_info, res.json())

    return render_template(
        'login-callback.html',
        user_name=user_info['name'],
        user_id=user_info['user_id'])