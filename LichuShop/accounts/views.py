from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer,ResetPasswordSerializer,loginSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def register(request):
    serializer=UserSerializer(data=request.data)
    if serializer.is_valid:
        serializer.save()
        return Response({"message":"user created successfully"},status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

@api_view(['POST'])
def login(request):
    serializer=loginSerializer(data=request.data)
    if serializer.is_valid:
        user=authenticate(email=serializer.validated_data['email'],password=serializer.validated_data['password'])
        if not user:
            return Response({"error": "Invalid credentials"}, status=400)
        
        refresh=RefreshToken.for_user(user)
        access_token=str(refresh.access_token)
        refresh_token=str(refresh)
        return Response({"message":"Login Successfully","access_token":access_token,"refresh_token":refresh_token})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    