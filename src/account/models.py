from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(BaseModel, AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  

