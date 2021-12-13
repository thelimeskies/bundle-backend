from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CommaSeparatedIntegerField
from django.db.models.fields.related import ForeignKey
# Create your models here.

class MonoId(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mono_id = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updrated_at = models.DateTimeField(auto_now=True)
    

class StatementRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=50)
    reason = models.CharField(max_length=250)

class SendStatement(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=50)
    timeline = models.CharField(max_length=20)
    statement = models.JSONField()
    reason = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
        
    
