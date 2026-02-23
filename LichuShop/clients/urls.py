from django.urls import path
from .views import order_create,orders
urlpatterns = [
    path('ordercreation/',order_create),
    path('order/',orders),
]
