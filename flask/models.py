from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime, timedelta

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    third_party_id = Column(String(256), nullable=False)
    access_key = Column(String(256), nullable=False)
    renew_key = Column(String(256), nullable=False)
    session = Column(String(256), nullable=False)
    expire_time = Column(DateTime, nullable=False)

    def public_user(this):
        return {
            'name': this.name
        }

    def session_is_expired(this):
        return datetime.utcnow()+timedelta(minutes=10) > this.expire_time