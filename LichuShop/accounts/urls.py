from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair,token_refresh,token_verify
from .views import account
urlpatterns = [
    path('account/',account,name='account'),
    path('api/token/', token_obtain_pair, name='token_obtain_pair'),
    path('api/token/refresh/', token_refresh, name='token_refresh'),
    path('api/token/verify/', token_verify, name='token_verify'),
]
