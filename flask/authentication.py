from flask import request, current_app, Blueprint, render_template
from database import db_session
from models import User
import requests
import google_auth
from datetime import datetime

authentication = Blueprint('authentication', __name__)

@authentication.route("/")
def main():
    data = {'testJsonKey': 'testJsonValue NEW'}
    response = make_response(jsonify(data))
    response.set_cookie('username', 'the username')
    return response

@authentication.route("/login")
def login():
    # new_user = User(
    #     name = 'test2',
    #     third_party = 'test2',
    #     third_party_id = 'test2',
    #     access_key = 'test2',
    #     renew_key = 'test2',
    #     session = 'test2',
    #     expire_time = datetime.utcnow()
    # )
    #
    # s = db_session()
    # s.begin()
    # s.add(new_user)
    # s.commit()

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

    # new_user = User(
    #     name = 'test',
    #     third_party = 'test',
    #     third_party_id = 'test',
    #     access_key = 'test',
    #     renew_key = 'test',
    #     session = 'test',
    #     expire_time = datetime.utcnow()
    # )
    #
    # print new_user

    # db_session.add(new_user)
    # db_session.commit()

    return render_template(
        'login-callback.html',
        user_name=user_info['name'],
        user_id=user_info['user_id'])