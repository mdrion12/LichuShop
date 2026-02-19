from dataclasses import field
from pyclbr import Class
from unittest.util import _MAX_LENGTH
from rest_framework import serializers

from clients.models import Product
from .models import user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=user
        fields='__all__'

class loginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

class ResetPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField(max_length=6)
    new_password=serializers.CharField(write_only=True)

class sendOtpSerializer(serializers.Serializer):
    email=serializers.EmailField()

class productListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'






