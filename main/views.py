from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from pymono import Mono
import os

from django.conf import settings
from django.core.mail import send_mail

from rest_framework import viewsets
from .serializer import MonoIdSerializer, StatementReqSerializer, SendStatementSerializer
from .models import MonoId, StatementRequest, SendStatement
from main import models


class MonoIDView(viewsets.ModelViewSet):
    
    queryset = MonoId.objects.all()
    serializer_class = MonoIdSerializer
    
    def list(self, request, *args, **kwargs):
        user_id = MonoId.objects.filter(user=request.user)
        serializer = MonoIdSerializer(user_id, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        mono_id = MonoId.objects.create(user=request.user, 
                                        mono_id=request.data['mono_id'], 
                                        account_name=request.data['account_name'])
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
    
    
class ReqStatementViewSet(viewsets.ModelViewSet):
    queryset = StatementRequest.objects.all()
    serializer_class = StatementReqSerializer
    
    def create(self, request, *args, **kwargs):
        req = StatementRequest.objects.create(sender=request.user, 
                                              receiver=request.data['receiver'],
                                              reason=request.data['reason'])
        serializer = StatementReqSerializer(req)
        
        subject = "You've Received Request to send Statement from {}".format(request.user.username)
        message = 'Hi {}, You have a Request to send your statement of Account for "{}".'.format(request.data['receiver'], request.data["reason"])
        email_from = settings.EMAIL_HOST_USER
        user = models.User.objects.filter(username=request.data['receiver']).values()
        try:
            recipient_list = [user[0]['email'], ]
            send_mail( subject, message, email_from, recipient_list )
            
            return Response(serializer.data)
        except:
            return Response({"error": "User does not Exist"})
    
    def list(self, request, *args, **kwargs):
        user_id = StatementRequest.objects.filter(receiver=request.user.username)
        serializer = StatementReqSerializer(user_id, many=True)
        return Response(serializer.data)
    
class SendStatementViewSet(viewsets.ModelViewSet):
    queryset = SendStatement.objects.all()
    serializer_class = SendStatementSerializer
    
    def list(self, request, *args, **kwargs):
        receiver_id = SendStatement.objects.filter(receiver=request.user.username)
        serializer = SendStatementSerializer(receiver_id, many=True)
        return Response(serializer.data)
        
    
    def create(self, request, *args, **kwargs):
        
        mono= Mono(request.data['mono_id'])
        (data,status) = mono.Auth()
        mono.SetUserId(data.get("id"))
        (data, status) = mono.getStatement(request.data['timeline'])
        
        
        send = SendStatement.objects.create(sender=request.user.username, 
                                        receiver=request.data['receiver'], 
                                        timeline=request.data['timeline'],
                                        reason = request.data['reason'],
                                        statement=data
                                        )

        return Response(SendStatementSerializer(send).data)
    
    