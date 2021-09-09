import uuid
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                            PermissionsMixin
from django.conf import settings


class Recipe(models.Model):
    """Recipe object"""
    name = models.TextField(blank=False)
    description = models.TextField(default='')

    def __str__(self):
        return self.name
