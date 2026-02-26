from dataclasses import field, fields
from itertools import product
from pyexpat import model
from statistics import quantiles
from tkinter.tix import Tree
from turtle import mode
from unittest.util import _MAX_LENGTH

from rest_framework import serializers
from .models import Customer, Order, Product

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

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'


class orderStatusserializer(serializers.Serializer):
    status=serializers.CharField(max_length=20)
        
class OrderProductSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=250)
    product_price = serializers.IntegerField()
    product_description = serializers.CharField(max_length=300)
    product_image = serializers.CharField(allow_null=True)
    quantity = serializers.IntegerField()
    total_price = serializers.IntegerField()    
    
class orderDetailSerializer(serializers.Serializer):
    customer_name=serializers.CharField(max_length=50)
    phone_number=serializers.CharField(max_length=11)
    address=serializers.CharField(max_length=11)
    productlist=OrderProductSerializer(many=True)
