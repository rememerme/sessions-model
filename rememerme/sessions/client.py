from rest_framework.test import APIClient

class SessionClient:
	@staticmethod
	def create(username, password):
		APIClient().post('/rest/v1/')