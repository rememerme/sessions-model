import requests
from rememerme.sessions.models import Session

class SessionClientError(Exception):
    pass

def strip_trailing_slash(url):
    if url[-1] == '/':
        return url[:-1]
    return url

class SessionClient:
    DEFAULT_URL = 'http://134.53.148.103:8000'

    def __init__(self, url=DEFAULT_URL):
        self.url = strip_trailing_slash(url)

    def create(self, username, password):
        payload = { 'username':username, 'password':password }
        r = requests.post(self.url + '/rest/v1/sessions',data=payload)
        if r.status_code is not 200:
            raise SessionClientError(r.text)
        return Session.fromMap(r.json())

    def update(self, session_id):
        r = requests.put(self.url + '/rest/v1/sessions/%s' % str(session_id))
        if r.status_code is not 200:
            raise SessionClientError(r.text)
        return Session.fromMap(r.json())
    
    def delete(self, session_id):
        r = requests.delete(self.url + '/rest/v1/sessions/%s' % str(session_id))
        if r.status_code is not 200:
            raise SessionClientError(r.text)
        return Session.fromMap(r.json())
