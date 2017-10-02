from flask import Flask, request, jsonify, make_response
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

@app.route("/")
def main():

    google_keys = getGoogleKeys()
    print(google_keys)

    json_dict = request.get_json()
    data = {'testJsonKey': 'testJsonValue NEW'}
    response = make_response(jsonify(data))
    response.set_cookie('username', 'the username')
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)

