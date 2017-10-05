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
    return render_template('login.html', login_url=google_auth.login_url)

@authentication.route("/login")
def login():
    return render_template('login.html', login_url=google_auth.login_url)

@authentication.route("/login-callback")
def login_callback():
    code = request.args.get('code')
    user_info = google_auth.get_user_keys(code)
    session_hash = user_controller.get_or_create_google_new(user_info)

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
    user = user_controller.return_valid_user(request.cookies.get('dmc_session'))
    new_session = None

    if user is not None:
        if user.session_is_expired():
            new_session = user_controller.renew_google_user(user)
        data = user.public_user()
    else:
        data = None

    response = make_response(jsonify(data))

    if new_session is not None:
        response.set_cookie('dmc_session', new_session)
    return response