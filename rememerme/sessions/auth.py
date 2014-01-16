from rest_framework import authentication, exceptions, HTTP_HEADER_ENCODING
from rememerme.sessions.client import SessionClientError, SessionClient

class AuthUser:
    def __init__(self, user_id):
        self.pk = user_id
        self.user_id = user_id

    def is_authenticated(self):
        return True

class RememermeAuthentication(authentication.BaseAuthentication):
    '''
        Custom Rememerme Authentication scheme used for all Django projects.
        
        Clients should authenticate by passing an access_token either as a query parameter or
        in the HTTP_AUTHORIZATION header. For example:
        
            NOMNOM:8000/rest/v1?access_token=b12736-8djfyeu-shdu-shsjjd
                                    OR
            Authorization: b12736-8djfyeu-shdu-shsjjd
    '''
    
    @staticmethod
    def get_authorization_header(request):
        '''
            Return request's 'Authorization:' header, as a bytestring.
            Hide some test client ickyness where the header can be unicode.
        '''
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if type(auth) == type(''):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth
    
    def authenticate(self, request):
        '''
            Uses the given access token (session_id) to convert the session
            into an active user.
        '''
        token = None
        
        if 'access_token' in request.QUERY_PARAMS and request.QUERY_PARAMS['access_token']:
            token = request.QUERY_PARAMS['access_token']
        
        if not token:
            token = RememermeAuthentication.get_authorization_header(request)
            
        if not token:    
            return None # return None when no authentication attempted
        
        # start the authentication process. If successful returning a tuple
        try:
            return (AuthUser(SessionClient.update(token).user_id), token)
        except SessionClientError:
            raise exceptions.AuthenticationFailed("Invalid access_token. No existing session.")
        
    def authenticate_header(self, request):
        return 'Rememerme/Token'
