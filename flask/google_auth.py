import os
import urlparse
from urllib import urlencode
import requests

def getGoogleKeys():
    google_keys = {}
    google_keys['client']=os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    google_keys['secret']=os.getenv('GOOGLE_OAUTH_SECRET')
    return google_keys

google_keys = getGoogleKeys()

def generate_login_url():
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    parsed_url = list(urlparse.urlparse(base_url))
    params = {
        'redirect_uri': 'http://localhost:8090/login-callback',
        'scope': 'profile',
        'access_type': 'offline',
        'response_type': 'code',
        'client_id': google_keys['client'],
        'prompt': 'consent'
    }
    parsed_url[4] = urlencode(params)
    return urlparse.urlunparse(parsed_url)

login_url = generate_login_url()

def generate_token_url(code):
    base_url = "https://www.googleapis.com/oauth2/v4/token"
    parsed_url = list(urlparse.urlparse(base_url))
    params = {
        'code': code,
        'client_id': google_keys['client'],
        'client_secret': google_keys['secret'],
        'redirect_uri': 'http://localhost:8090/login-callback',
        'grant_type': 'authorization_code'
    }
    parsed_url[4] = urlencode(params)
    return urlparse.urlunparse(parsed_url)

def generate_renew_url(refresh_token):
    base_url = "https://www.googleapis.com/oauth2/v4/token"
    parsed_url = list(urlparse.urlparse(base_url))
    params = {
        'refresh_token': refresh_token,
        'client_id': google_keys['client'],
        'client_secret': google_keys['secret'],
        'grant_type': 'refresh_token'
    }
    parsed_url[4] = urlencode(params)
    return urlparse.urlunparse(parsed_url)

def get_user_info(token):
    user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo?alt=json&access_token='+token
    res = requests.get(user_info_url)
    return {'user_id': res.json()['sub'], 'name': res.json()['name']}

def get_user_keys(code):
    token_url = generate_token_url(code)
    res = requests.post(token_url)
    access_token = res.json()['access_token']
    expires_in = res.json()['expires_in']
    refresh_token = res.json()['refresh_token']

    print '\n\n\nget keys', res.json()

    user_info = get_user_info(access_token)
    user_info['access_token'] = access_token
    user_info['expires_in'] = expires_in
    user_info['refresh_token'] = refresh_token

    return user_info

def refresh_user_keys(renew_key):
    renew_url = generate_renew_url(renew_key)
    res = requests.post(renew_url)
    access_token = res.json()['access_token']
    expires_in = res.json()['expires_in']

    print '\n\n\nrefresh keys', res.json()

    user_info = get_user_info(access_token)
    user_info['access_token'] = access_token
    user_info['expires_in'] = expires_in

    return user_info
