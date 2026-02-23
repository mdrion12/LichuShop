from dataclasses import field, fields
from itertools import product
from pyexpat import model
from statistics import quantiles
from tkinter.tix import Tree

from rest_framework import serializers
from .models import Customer, Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields='__all__'
        extra_kwargs = {
            'phone_number': {'validators': []}
        }

class productSerializer(serializers.Serializer):
    product_id=serializers.IntegerField()
    quantity=serializers.IntegerField()

class OrderCreationSerializer(serializers.Serializer):
    Customer=CustomerSerializer()
    product=productSerializer(many=True)

class orderserilizer(serializers.ModelSerializer):
    phone_number=CustomerSerializer()
    class Meta:
        model=Order
        fields='__all__'