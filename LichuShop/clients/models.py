from asyncio.windows_events import NULL
from tarfile import NUL
from typing import Required
from django.db import models
# Create your models here
class Customer(models.Model):
    name=models.CharField(max_length=100)
    phone_number=models.CharField(primary_key=True)
    address=models.CharField(max_length=100)
    datetime=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name}-{self.phone_number}"

class Product(models.Model):
    id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=250)
    product_image=models.ImageField(upload_to='products/', null=True, blank=True)
    product_description=models.CharField(max_length=300)
    price=models.IntegerField()
    stock=models.IntegerField()
    is_active=models.BooleanField(default=True)
    def __str__(self):
        return f"{self.id}-{self.product_name}"

class order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('delivered', 'Delivered'),
    ]
    id=models.AutoField(primary_key=True)
    phone_number=models.ForeignKey(Customer,on_delete=models.CASCADE)
    total_price=models.IntegerField()
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.phone_number.name}-{self.status}"

class order_item(models.Model):
    order_id=models.ForeignKey(order,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.IntegerField()
    def __str__(self):
        return f"{self.product_id.product_name}-{self.quantity}"