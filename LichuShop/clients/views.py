from django.shortcuts import render
from django.contrib.auth import get_user_model
# Create your views here.
User=get_user_model()
def change(request):
  user = User.objects.get(username='admin') 
  user.set_password('new_password_here')
  user.save()
  print("Password changed successfully!")