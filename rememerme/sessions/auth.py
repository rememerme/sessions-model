from rememerme.users.models import User
from rest_framework import authentication, exceptions

class RememermeAuthentication(authentication.BaseAuthentication):
	def authenticate(self, request):
		pass
