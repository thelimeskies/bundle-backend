from django.db.models import fields
from rest_framework import serializers
from .models import MonoId, StatementRequest, SendStatement

class MonoIdSerializer(serializers.ModelSerializer):
    mono_id = serializers.CharField(max_length=100)
    class Meta:
        model = MonoId
        fields = ('id', 'mono_id', 'account_name')
        
class StatementReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementRequest
        fields = ('id', 'receiver', 'reason')

class SendStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendStatement
        fields = ('id', 'sender', 'receiver', 'timeline', 'statement', 'reason')
        
from django.conf import settings

from rest_framework import serializers
from rest_auth.models import TokenModel
from rest_auth.utils import import_callable
from rest_auth.serializers import UserDetailsSerializer as DefaultUserDetailsSerializer

# This is to allow you to override the UserDetailsSerializer at any time.
# If you're sure you won't, you can skip this and use DefaultUserDetailsSerializer directly
rest_auth_serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})
UserDetailsSerializer = import_callable(
    rest_auth_serializers.get('USER_DETAILS_SERIALIZER', DefaultUserDetailsSerializer)
)

class CustomTokenSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)

    class Meta:
        model = TokenModel
        fields = ('key', 'user', )