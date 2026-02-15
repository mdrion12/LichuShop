from django.contrib import admin
from .models import Customer,Product,order,order_item

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(order)
admin.site.register(order_item)

