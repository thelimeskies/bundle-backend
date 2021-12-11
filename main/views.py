from django.shortcuts import render
from pymono import Mono
import os

from rest_framework import viewsets
from .serializer import MonoIdSerializer
from .models import MonoId

class MonoIdViewSet(viewsets.ModelViewSet):
    queryset = MonoId.objects.all()
    serializer_class = MonoIdSerializer


"""os.environ['MONO-SEC-KEY'] = ""

mono= Mono('code_0DalxrBkFktxPBJkzsuV')
(data,status) = mono.Auth()
mono.SetUserId(data.get("id"))
print(mono.getStatement("last12month","pdf"))"""