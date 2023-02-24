from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class User(AbstractUser):
    profile_photo = models.CharField(
        max_length=240, default='', blank=True, null=True)
    profile_bg_photo = models.CharField(
        max_length=240, default='', blank=True, null=True)
    bio = models.TextField(default='', blank=True, null=True)

    # objects = BaseUserManager()
