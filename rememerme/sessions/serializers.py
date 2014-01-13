from models import User
from rest_framework import serializers

'''
    The Sesssion serializer used to display a model to the web through json serialization.
'''
class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('session_id', 'user_id', 'date_created', 'last_modified')