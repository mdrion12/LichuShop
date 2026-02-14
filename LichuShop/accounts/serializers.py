from rest_framework import serializers
from .models import user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=user
        fields='__all__'
    def create(self, validated_data):
       password = validated_data.pop('password')
       User = user(**validated_data)
       User.set_password(password)
       User.save()
       return User

class loginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

class ResetPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField(max_length=6)
    new_password=serializers.CharField(write_only=True)