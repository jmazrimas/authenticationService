from flask import Flask
from database import init_engine, init_db


def init_app():
    print 'init app called'
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://authentication:authenticationpass@localhost/authentication'
    init_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    init_db()
    from authentication import authentication
    app.register_blueprint(authentication)

    return app

if __name__ == '__main__':
    app = init_app()
    app.run(host='0.0.0.0', port=8090, debug=True)