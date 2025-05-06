from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=25,null=True,unique=True)
    middle_name = models.CharField(max_length=50,null=True,blank=True)
    telephone = models.CharField(max_length=10,null=False)
    email = models.EmailField(max_length=255,null=False,unique=True)
    secret_code = models.CharField(max_length=32,null=True,blank=True)
    otp_code = models.CharField(max_length=6,null=True,blank=True)

    is_active = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)