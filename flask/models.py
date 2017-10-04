from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    third_party = db.Column(db.String(256), nullable=False)
    third_party_id = db.Column(db.String(256), nullable=False)
    access_key = db.Column(db.String(256), nullable=False)
    renew_key = db.Column(db.String(256), nullable=False)
    session = db.Column(db.String(256), nullable=False)
    expire_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name