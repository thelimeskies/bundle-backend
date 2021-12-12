from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CommaSeparatedIntegerField
# Create your models here.

class MonoId(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mono_id = models.CharField(max_length=20)
    account_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updrated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.pk
    
