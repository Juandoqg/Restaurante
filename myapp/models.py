from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Tus propiedades personalizadas
    is_chef = models.BooleanField(default=False)
    is_waiter = models.BooleanField(default=False)