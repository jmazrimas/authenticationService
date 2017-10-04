from flask import Flask, request, jsonify, make_response, render_template
import socket
import requests
import google_auth
from authentication_data_model import AuthenticationDataModel

app = Flask(__name__)
adm = AuthenticationDataModel(app)

@app.route("/")
def main():
    data = {'testJsonKey': 'testJsonValue NEW'}
    response = make_response(jsonify(data))
    response.set_cookie('username', 'the username')
    return response

@app.route("/login")
def login():
    return render_template('login.html', login_url=google_auth.login_url)

@app.route("/login-callback")
def login_callback():
    code = request.args.get('code')
    token_url = google_auth.generate_token_url(code)
    res = requests.post(token_url)
    access_token = res.json()['access_token']
    expires_in = res.json()['expires_in']
    refresh_token = res.json()['refresh_token']

    user_info = google_auth.get_user_info(access_token)

    return render_template(
        'login-callback.html',
        user_name=user_info['name'],
        user_id=user_info['user_id'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)

