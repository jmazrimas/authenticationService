from flask import Flask, request, jsonify, make_response, render_template
import urlparse
from urllib import urlencode
import os
import socket
import requests

# Connect to Redis
# redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

def getGoogleKeys():
    google_keys = {}
    google_keys['client']=os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    google_keys['secret']=os.getenv('GOOGLE_OAUTH_SECRET')
    return google_keys

google_keys = getGoogleKeys()

def generate_login_url():
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    parsed_url = list(urlparse.urlparse(base_url))
    params = {
        'redirect_uri': 'http://localhost:8090/login-callback',
        'scope': 'profile',
        'access_type': 'offline',
        'response_type': 'code',
        'client_id': google_keys['client'],
        'prompt': 'consent'
    }
    parsed_url[4] = urlencode(params)
    return urlparse.urlunparse(parsed_url)

login_url = generate_login_url()
print '\n\n\n\nLOGIN URL', login_url

def generate_token_url(code):
    base_url = "https://www.googleapis.com/oauth2/v4/token"
    parsed_url = list(urlparse.urlparse(base_url))
    params = {
        'code': code,
        'client_id': google_keys['client'],
        'client_secret': google_keys['secret'],
        'redirect_uri': 'http://localhost:8090/login-callback',
        'grant_type': 'authorization_code'
    }
    parsed_url[4] = urlencode(params)
    return urlparse.urlunparse(parsed_url)

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
    return render_template('login.html', login_url=login_url)

@app.route("/login-callback")
def login_callback():
    code = request.args.get('code')
    token_url = generate_token_url(code)
    res = requests.post(token_url)
    access_token = res.json()['access_token']
    expires_in = res.json()['expires_in']
    refresh_token = res.json()['refresh_token']

    print 'access_token:', access_token
    print 'expires_in:', expires_in
    print 'refresh_token:', refresh_token

    return render_template('login-callback.html', login_url=login_url)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)

