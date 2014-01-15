import requests
from rememerme.sessions.models import Session
from rest_framework.exceptions import APIException

class YouDunFucked(APIException):
	pass

class SessionClient:
	@staticmethod
	def create(username, password):
		payload = {'username':username, 'password':password}
		r = requests.post('http://134.53.148.103:8000/rest/v1/',data=payload)
		if r is not 200:
			raise YouDunFucked()
		return Session.fromMap(r.json())

	@staticmethod
	def update(session_id):
		r = requests.put('http://134.53.148.103:8000/rest/v1/%s' % str(session_id) )
		if r is not 200:
			raise YouDunFucked()
		return Session.fromMap(r.json())
