from django.db import models
import random
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
class user(AbstractUser):
    email=models.EmailField(unique=True)
    phone_number=models.CharField(max_length=11)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return f"{self.username} - {self.email}"
    

class ResetPassword(models.Model):
    user=models.OneToOneField(user,on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)
    created=models.DateTimeField(auto_now_add=True)
    verified=models.BooleanField(default=False)

    def generate_otp(self):
        self.otp=str(random.randint(100000,999999))
        self.created=timezone.now()
        self.verified=False
        self.save()
        return self.otp
    def __str__(self):
        return f"{self.user.username} - {self.otp}"

