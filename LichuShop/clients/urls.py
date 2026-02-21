from django.urls import path
from .views import order_create
urlpatterns = [
    path('ordercreation/',order_create),
]
