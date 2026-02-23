from django.urls import path
from .views import order_create,orders,orderstatus
urlpatterns = [
    path('ordercreation/',order_create),
    path('order/',orders),
    path('order/<str:order_status>/',orderstatus),
]
