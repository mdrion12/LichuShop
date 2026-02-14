from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer,loginSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import user,ResetPassword
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
User=get_user_model()
@api_view(['POST'])
def register(request):
    
    serializer=UserSerializer(data=request.data)
    
    if User.objects.exist():
        return Response({"message":"user already exist! try to another way"},status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"},status=status.HTTP_201_CREATED)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh=request.data.get("refresh")
        if not refresh:
              return Response({"error": "Refresh token missing"}, status=status.HTTP_400_BAD_REQUEST)
        refresh_token=RefreshToken(refresh)
        refresh_token.blacklist()
        return Response({"message": "Logout successful"},status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def send_otp(request):
    email=request.data.get("email")
    if not email:
        return Response({"error": "Email required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user=User.objects.get(email=email)
    except Exception as e:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    reset_otp=ResetPassword(user=user)
    otp=reset_otp.generate_otp()
    send_mail(
        subject="Your Password Reset OTP",
        message=f"Your OTP is: {otp}",
        from_email="noreply@example.com",
        recipient_list=[email],
        fail_silently=False,
    )
    return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)


   
