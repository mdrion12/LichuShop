from django.urls import path
from .views import productCreate, register,login,logout,send_otp,reset_password,productUpdatedelete,productList,order
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,

)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/',register, name='register'),
    path('login/',login,name="login"),
    path('logout/',logout,name='logout'),
    path('send_otp/',send_otp,name='send_otp'),
    path('reset_password/',reset_password,name='reset_password'),
    path('productCreate/',productCreate,name='productCreate'),
    path('productUpdate/<int:id>/',productUpdatedelete,name='update_product'),
    path('productList/',productList,name='productList'),
    path('order/',order,name='order'),

    
]
