from flask import Flask, request, jsonify, make_response, render_template
import urlparse
from urllib import urlencode
import os
import socket

# Connect to Redis
# redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

def getGoogleKeys():
    google_keys = {}
    google_keys['client']=os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    google_keys['secret']=os.getenv('GOOGLE_OAUTH_SECRET')
    return google_keys

google_keys = getGoogleKeys()

def generateLoginURL():
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    parsed_url = list(urlparse.urlparse(base_url))
    params = {
        'redirect_uri': 'http://localhost:8090/login-callback',
        'response_type': 'code',
        'client_id': google_keys['client'],
        'scope': 'profile'
    }
    parsed_url[4] = urlencode(params)
    return urlparse.urlunparse(parsed_url)

loginURL = generateLoginURL()

@app.route("/")
def main():

    print(google_keys)

    json_dict = request.get_json()
    data = {'testJsonKey': 'testJsonValue NEW'}
    response = make_response(jsonify(data))
    response.set_cookie('username', 'the username')
    return response

@app.route("/login")
def login():
    return render_template('login.html', loginURL=loginURL)

@app.route("/login-callback")
def login_callback():
    return render_template('login-callback.html', loginURL=loginURL)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)

