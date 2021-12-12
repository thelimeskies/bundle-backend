from django.contrib import admin
from .models import MonoId, SendStatement, StatementRequest

# Register your models here.
admin.site.register(MonoId)
admin.site.register(SendStatement)
admin.site.register(StatementRequest)
