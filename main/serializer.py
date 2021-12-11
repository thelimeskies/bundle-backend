from rest_framework import serializers
from .models import MonoId

class MonoIdSerializer(serializers.ModelSerializer):
    mono_id = serializers.CharField(max_length=100)
    class Meta:
        model = MonoId
        fields = ('id', 'mono_id')