from database import db_session
from models import User
from datetime import datetime, timedelta
import hashlib, struct
import google_auth

def hash_key(key):
    hash = hashlib.sha256()
    hash.update(struct.pack("I", len(key)))
    hash.update(key)
    return hash.hexdigest()

def update_user_keys(existing_user, new_keys):
    existing_user.access_key = new_keys['access_key']
    if 'renew_key' in new_keys:
        existing_user.renew_key = new_keys['renew_key']
    existing_user.session = new_keys['session']
    existing_user.expire_time = datetime.utcnow()+timedelta(0,new_keys['expire_time'])
    return existing_user

def session_is_valid(existing_user):
    return datetime.utcnow()+timedelta(minutes=10) < existing_user.expire_time

def return_valid_user(session_hash):
    s = db_session()
    s.begin()
    existing_user = s.query(User).filter_by(session = session_hash).first()
    s.commit()
    if existing_user:
        if session_is_valid(existing_user):
            return existing_user.public_user()
        else:
            renewed_user_info = google_auth.refresh_user_keys(existing_user.renew_key)
            renewed_user_info = map_google_user_data(renewed_user_info)
            s.begin()
            update_user_keys(existing_user, renewed_user_info)
            s.commit()
            return existing_user.public_user()
    else:
        return None

def google_user_model(user_data):

    google_user = User(
            name = user_data['name'],
            third_party_id = user_data['user_id']+'@google.com',
            access_key = user_data['access_token'],
            renew_key = user_data['refresh_token'],
            session = hash_key(user_data['access_token']),
            expire_time = datetime.utcnow()+timedelta(0,user_data['expires_in'])
        )

    return google_user

def map_google_user_data(user_data):
    mapped_user = {
        'access_key': user_data['access_token'],
        'session': hash_key(user_data['access_token']),
        'expire_time': user_data['expires_in']
    }
    if 'refresh_token' in user_data:
        mapped_user['renew_key'] = user_data['refresh_token']

    return mapped_user

def get_or_create_google_new(user_data):
    s = db_session()
    s.begin()
    existing_user = s.query(User).filter_by(third_party_id = user_data['user_id']+'@google.com').first()

    if existing_user:
        user_session = update_user_keys(existing_user, map_google_user_data(user_data)).session
    else:
        new_user = create_google_user(user_data, s)
        user_session = new_user.session

    s.commit()
    return user_session

def create_google_user(user_data, db_session):
    new_user = google_user_model(user_data)
    db_session.add(new_user)
    return new_user