from rememerme.sessions.cassa import CassaModel
from django.db import models
import pycassa
from django.conf import settings
import uuid
from rest_framework import serializers
import datetime
import dateutil.parser

# User model faked to use Cassandra
POOL = pycassa.ConnectionPool('users', server_list=settings.CASSANDRA_NODES)

class Session(CassaModel):
    table = pycassa.ColumnFamily(POOL, 'session')
    
    session_id = models.TextField(primary_key=True)
    user_id = models.TextField()
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()

    '''
        Creates a Session object from a map object with the properties.
    '''
    @staticmethod
    def fromMap(mapRep):
        return Session(**mapRep)
    
    '''
        Creates a Session object from the tuple return from Cassandra.
    '''
    @staticmethod
    def fromCassa(cassRep):
        mapRep = {key : val for key, val in cassRep[1].iteritems()}
        mapRep['session_id'] = str(cassRep[0])
        
        return Session.fromMap(mapRep)
    
    '''
        Method for getting single sessions from cassandra given the session_id.
    '''
    @staticmethod
    def get(session_id=None):
        if session_id:
            return Session.getByID(session_id)
        
        return None
    
    '''
        Gets the session given an ID.
        
        @param session_id: The uuid of the session.
    '''
    @staticmethod
    def getByID(session_id):
        if not isinstance(session_id, uuid.UUID):
            session_id = uuid.UUID(session_id)
        return Session.fromCassa((str(session_id), Session.table.get(session_id)))
   
    '''
        Gets all of the users and uses an offset and limit if
        supplied.
        
        @param offset: Optional argument. Used to offset the query by so
            many entries.
        @param limit: Optional argument. Used to limit the number of entries
            returned by the query.
    '''
    @staticmethod
    def all(limit=settings.REST_FRAMEWORK['PAGINATE_BY'], page=None):
        if not page:
            return [User.fromCassa(cassRep) for cassRep in User.table.get_range(row_count=limit)]
        else:
            if not isinstance(page, uuid.UUID):
                page = uuid.UUID(page)
            gen = User.table.get_range(start=page, row_count=limit + 1)
            gen.next()
            return [User.fromCassa(cassRep) for cassRep in gen]
    
    '''
        Saves a set of users given by the cassandra in/output, which is
        a dictionary of values.
        
        @param users: The set of users to save to the user store.  
    '''
    def save(self):
        session_id = uuid.uuid1() if not self.session_id else uuid.UUID(self.session_id)
        Session.table.insert(session_id, CassaSessionSerializer(self).fix_data())
        self.session_id = str(session_id)
        

    def delete(self):
        Session.table.remove(uuid.UUID(self.session_id))
        
'''
    The User serializer used to create a python dictionary for submitting to the
    Cassandra database with the correct options.
'''
class CassaSessionSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format='iso-8601', source='date_created')
    last_modified = serializers.DateTimeField(format='iso-8601', source='last_modified')
    
    class Meta:
        model = Session
        fields = ('user_id', 'date_created', 'last_modified')

    def fix_data(self):
        data = self.data
        data['user_id'] = uuid.UUID(data['user_id']) 
        data['date_created'] = dateutil.parser.parse(data['date_created']) 
        data['last_modified'] = dateutil.parser.parse(data['last_modified'])
        return data
    
