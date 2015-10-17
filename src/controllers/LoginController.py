from flask import session
from ..core.messager import TweetAdapter
import tweepy

def getStartingUrl():
    api = TweetAdapter.createAPIObject()
    url = api.auth.get_authorization_url()
    session['requestToken'] = api.auth.request_token
    return url

def getAuth(verifier, token):
    api = TweetAdapter.createAPIObject()
    print(session['requestToken'])
    api.auth.request_token = session['requestToken']
    session.pop('requestToken')
    print(verifier, token)
    authentications = api.auth.get_access_token(verifier)
    return api.auth.access_token, api.auth.access_token_secret
