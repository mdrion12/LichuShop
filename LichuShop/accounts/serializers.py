from rest_framework import serializers
from .models import user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=user
        fields='__all__'

class loginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
