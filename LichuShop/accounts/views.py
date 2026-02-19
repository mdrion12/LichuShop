from functools import partial
from pickle import TRUE
from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import is_valid_path
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response

from clients.models import Product
from .serializers import UserSerializer,loginSerializer,ResetPasswordSerializer, sendOtpSerializer,productListSerializer
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
    
    if User.objects.exists():
        return Response({"message":"user already exist! try to another way"},status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        user_data=serializer.validated_data
        password=user_data.pop("password")
        user=User(**user_data)
        user.set_password(password)
        user.save()
        return Response({"message": "User created successfully"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

@api_view(['POST'])
def login(request):
    serializer=loginSerializer(data=request.data)
    if serializer.is_valid():
        email=serializer.validated_data['email']
        password=serializer.validated_data['password']
        user=authenticate(email=email,password=password)
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
    serializer=sendOtpSerializer(data=request.data)
    if serializer.is_valid():
        email=serializer.validated_data["email"]
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        send_otp,_=ResetPassword.objects.get_or_create(user=user)
        otp=send_otp.generate_otp()
        send_mail(
            subject="Your Password Reset OTP",
            message=f"Your OTP is: {otp}",
            from_email="noreply@example.com",
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reset_password(request):
    serializer=ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email=serializer.validated_data['email']
        otp=serializer.validated_data['otp']
        new_password=serializer.validated_data['new_password']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            reset_obj, _ = ResetPassword.objects.get_or_create(user=user)
        except ResetPassword.DoesNotExist:
            return Response({"error": "Reset request not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if reset_obj.otp!=otp:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        reset_obj.verified = True
        reset_obj.save()
        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def productCreate(request):
    serializer=productListSerializer(data=request.data)
    if request.method=='POST':
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','PATCH','DELETE','GET'])
@permission_classes([IsAuthenticated])
def productUpdatedelete(request,id):
    try:
        product=Product.objects.get(id=id)
    except Exception as e:
        return Response({"message :":"product not found"},status=status.HTTP_404_NOT_FOUND)
    partial=True
    if request.method=='PUT':
        partial=False
    if request.method=='DELETE':
        product.delete()
        return Response({"message :":"product deleted successfully"})
    serializer=productListSerializer(product,data=request.data,partial=partial)
    if serializer.is_valid():
      serializer.save()
      return Response({"message :":"product updated successfully"})
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def productList(request):
    products = Product.objects.all()
    serializer = productListSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)





