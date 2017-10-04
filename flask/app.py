# from flask import Flask, request, jsonify, make_response, render_template
# import socket
# import requests
# import google_auth
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://authentication:authenticationpass@localhost/authentication'
# db = SQLAlchemy(app)
#
# import models
#
# db.create_all()
#
# @app.route("/")
# def main():
#     data = {'testJsonKey': 'testJsonValue NEW'}
#     response = make_response(jsonify(data))
#     response.set_cookie('username', 'the username')
#     return response
#
# @app.route("/login")
# def login():
#     return render_template('login.html', login_url=google_auth.login_url)
#
# @app.route("/login-callback")
# def login_callback():
#     code = request.args.get('code')
#     token_url = google_auth.generate_token_url(code)
#     res = requests.post(token_url)
#     access_token = res.json()['access_token']
#     expires_in = res.json()['expires_in']
#     refresh_token = res.json()['refresh_token']
#
#     user_info = google_auth.get_user_info(access_token)
#
#     return render_template(
#         'login-callback.html',
#         user_name=user_info['name'],
#         user_id=user_info['user_id'])
#
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=8090)
#


from flask import Flask
# from database import init_engine, init_db


def init_app():
    print 'init app called'
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://authentication:authenticationpass@localhost/authentication'
    # init_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    # init_db()
    from authentication import authentication
    app.register_blueprint(authentication)

    return app

if __name__ == '__main__':
    app = init_app()
    app.run(host='0.0.0.0', port=8090, debug=True)