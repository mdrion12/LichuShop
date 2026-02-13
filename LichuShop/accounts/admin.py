from django.contrib import admin
from . models import user,ResetPassword
# Register your models here.
admin.site.register(user)
admin.site.register(ResetPassword)
