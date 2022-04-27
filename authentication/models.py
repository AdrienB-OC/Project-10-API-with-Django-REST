from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32, default=email)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
