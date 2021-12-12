from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from pymono import Mono
import os

from rest_framework import viewsets
from .serializer import MonoIdSerializer
from .models import MonoId

os.environ['MONO-SEC-KEY'] = "test_sk_xCkpAQF17YYbbHlal3Ez"

class MonoIDView(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = MonoId.objects.all()
    serializer_class = MonoIdSerializer
    
    def list(self, request, *args, **kwargs):
        user_id = MonoId.objects.filter(user=request.user)
        serializer = MonoIdSerializer(user_id, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        mono_id = MonoId.objects.create(user=request.user, mono_id=request.data['mono_id'])
        return Response(MonoIdSerializer(mono_id).data)
    
class Transactions(APIView):
    authentication_classes = (TokenAuthentication,)
    
    def post(self, request, *args, **kwargs):
        try:
            mono_id = request.data['mono_id']
        except KeyError:
            return Response({'error': 'mono_id is required'})
        
        mono= Mono(mono_id)
        (data,status) = mono.Auth()
        mono.SetUserId(data.get("id"))
        data, status = mono.getTransactions(paginate=False)
        return Response({"status": "Success", "data": data})
    
class Statement(APIView):
    authentication_classes = (TokenAuthentication,)
    
    def post(self, request, *args, **kwargs):
        try:
            mono_id = request.data['mono_id']
            month = request.data['month']
        except KeyError:
            return Response({'error': 'mono_id and month is required'})
        
        mono= Mono(mono_id)
        (data,status) = mono.Auth()
        mono.SetUserId(data.get("id"))
        data, status = mono.getStatement(month)
        return Response({"status": "Success", "data": data})
    
class Credits(APIView):
    authentication_classes = (TokenAuthentication,)
    
    def post(self, request, *args, **kwargs):
        try:
            mono_id = request.data['mono_id']
        except KeyError:
            return Response({'error': 'mono_id is required'})
        
        mono= Mono(mono_id)
        (data,status) = mono.Auth()
        mono.SetUserId(data.get("id"))
        data, status = mono.getCredits()
        return Response({"status": "Success", "data": data})

class Debits(APIView):
    authentication_classes = (TokenAuthentication,)
    
    def post(self, request, *args, **kwargs):
        try:
            mono_id = request.data['mono_id']
        except KeyError:
            return Response({'error': 'mono_id is required'})
        
        mono= Mono(mono_id)
        (data,status) = mono.Auth()
        mono.SetUserId(data.get("id"))
        data, status = mono.getDebits()
        return Response({"status": "Success", "data": data})

class Account(APIView):
    authentication_classes = (TokenAuthentication,)
    
    def post(self, request, *args, **kwargs):
        try:
            mono_id = request.data['mono_id']
        except KeyError:
            return Response({'error': 'mono_id is required'})
        
        mono= Mono(mono_id)
        (data,status) = mono.Auth()
        mono.SetUserId(data.get("id"))
        data, status = mono.getAccount()
        return Response({"status": "Success", "data": data})

    