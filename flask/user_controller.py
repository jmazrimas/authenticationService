from database import db_session
from models import User
from datetime import datetime, timedelta
import hashlib, struct

def hash_key(key):
    hash = hashlib.sha256()
    hash.update(struct.pack("I", len(key)))
    hash.update(key)
    return hash.hexdigest()

def update_user_keys(existing_user, new_user):
    existing_user.access_key = new_user.access_key
    existing_user.renew_key = new_user.renew_key
    existing_user.session = new_user.session
    existing_user.expire_time = new_user.expire_time

def update_or_create(new_user):

    s = db_session()
    s.begin()

    existing_user = s.query(User).filter_by(third_party_id = new_user.third_party_id).first()

    if existing_user:
        update_user_keys(existing_user, new_user)
    else:
        s.add(new_user)

    s.commit()

    return new_user.session

def session_is_valid(existing_user):
    time_to_expire = existing_user.expire_time - datetime.utcnow()
    return time_to_expire.seconds > 100

def return_valid_user(session_hash):
    s = db_session()
    s.begin()
    existing_user = s.query(User).filter_by(session = session_hash).first()
    s.commit()
    if existing_user:
        if session_is_valid(existing_user):
            return existing_user.public_user()
        return None
    else:
        return None

def google_user_model(user_data):

    print 'expires in', user_data['expires_in']

    google_user = User(
            name = user_data['name'],
            third_party_id = user_data['user_id']+'@google.com',
            access_key = user_data['access_token'],
            renew_key = user_data['refresh_token'],
            session = hash_key(user_data['access_token']),
            expire_time = datetime.utcnow()+timedelta(0,user_data['expires_in'])
        )

    return google_user

def get_or_create_google(user_data):
    google_user = google_user_model(user_data)
    return update_or_create(google_user)