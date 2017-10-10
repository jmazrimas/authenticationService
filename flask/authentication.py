from flask import request, current_app, Blueprint, render_template, make_response, jsonify, redirect
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
    try:
        code = request.args.get('code')
        user_info = google_auth.get_user_keys(code)
        session_hash = user_controller.get_or_create_google_new(user_info)

        redirect_to_index = redirect('/signonservice/login-success')
        response = make_response(redirect_to_index)
        response.set_cookie('dmc_session', session_hash)
    except:
        redirect_to_index = redirect('/signonservice/login-failure')
        response = make_response(redirect_to_index)

    return response

@authentication.route("/login-success")
def login_success():
    user = user_controller.return_valid_user(request.cookies.get('dmc_session'))

    response = make_response(
        render_template(
        'login-callback.html',
        user_name=user.name,
        user_id=user.third_party_id)
    )

    return response

@authentication.route("/login-failure")
def login_failure():
    response = make_response(
        render_template(
        'login-failure.html'
        )
    )

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
        data = {}

    response = make_response(jsonify(data))

    if new_session is not None:
        response.set_cookie('dmc_session', new_session)
    return response