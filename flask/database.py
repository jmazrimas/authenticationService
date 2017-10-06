from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, create_session
from sqlalchemy.ext.declarative import declarative_base
import mysql.connector

engine = None
db_session = scoped_session(lambda: create_session(bind=engine))

Base = declarative_base()
#Base.query = db_session.query_property()

def init_engine(uri, **kwargs):
    global engine
    engine = create_engine(uri, **kwargs)
    return engine

def init_db():
    from models import User
    Base.metadata.create_all(bind=engine)