# from flask_sqlalchemy import SQLAlchemy
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(256), nullable=False)
#     third_party = db.Column(db.String(256), nullable=False)
#     third_party_id = db.Column(db.String(256), nullable=False)
#     access_key = db.Column(db.String(256), nullable=False)
#     renew_key = db.Column(db.String(256), nullable=False)
#     session = db.Column(db.String(256), nullable=False)
#     expire_time = db.Column(db.DateTime, nullable=False)
#
#     def __repr__(self):
#         return '<User %r>' % self.name


from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    third_party = Column(String(256), nullable=False)
    third_party_id = Column(String(256), nullable=False)
    access_key = Column(String(256), nullable=False)
    renew_key = Column(String(256), nullable=False)
    session = Column(String(256), nullable=False)
    expire_time = Column(DateTime, nullable=False)