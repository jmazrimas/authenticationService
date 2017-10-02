from flask import Flask, request, jsonify, make_response
import os
import socket

# Connect to Redis
# redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def main():
    # try:
    #     visits = redis.incr("counter")
    # except RedisError:
    #     visits = "<i>cannot connect to Redis, counter disabled</i>"

    # html = "<h3>Hello {name}!</h3>" \
    #        "<b>Hostname:</b> {hostname}<br/>" \
    #        "<b>Visits:</b> {visits}"
    # return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)
    json_dict = request.get_json()


    data = {'testJsonKey': 'testJsonValue NEW'}
    # return jsonify(data)

    response = make_response(jsonify(data))
    response.set_cookie('username', 'the username')
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)