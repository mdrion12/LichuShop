from django.urls import path
from .views import order_create,orders,orderstatus,order_details,order_Status_change
urlpatterns = [
    path('ordercreation/',order_create),
    path('order/',orders),
    path('order/<str:order_status>/',orderstatus),
    path('orderdetails/<int:order_id>/',order_details),
    path('order_Status_change/<int:order_id>/<str:order_status>/',order_Status_change),
]
