from rest_framework import serializers
from .models import MonoId

class MonoIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonoId
        fields = ('id', 'user', 'mono_id')