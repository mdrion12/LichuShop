from rest_framework import serializers
from .models import user,ResetPassword

class UserSerializer(serializers.ModelSerializer):
    class meta:
        model=user
        fields='__all__'


class ResetPasswordSerializer(serializers.ModelSerializer):
    class meta:
        model=ResetPassword
        fields='__all__'

class loginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
