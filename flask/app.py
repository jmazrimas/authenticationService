from flask import Flask
import mysql.connector
from database import init_engine, init_db
import os

def init_app():
    print 'init app called'
    db_name = os.environ['AUTH_SVC_DB_NAME']
    db_user = os.environ['AUTH_SVC_DB_USER']
    db_pass = os.environ['AUTH_SVC_DB_PASS']

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://'+db_user+':'+db_pass+'@authentication-mariadb/'+db_name
    init_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    init_db()
    from authentication import authentication
    app.register_blueprint(authentication, url_prefix='/signonservice')

    return app

if __name__ == '__main__':
    app = init_app()
    app.run(host='0.0.0.0', port=8090, debug=True)