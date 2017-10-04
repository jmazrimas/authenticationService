from flask_sqlalchemy import SQLAlchemy

class AuthenticationDataModel:
    def __init__(self, app):
        self.app = app

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://authentication:authenticationpass@localhost/authentication'
        db = SQLAlchemy(app)
        self.db = db

        class User(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(80), unique=True, nullable=False)

            def __repr__(self):
                return '<User %r>' % self.name

        db.create_all()