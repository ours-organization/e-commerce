from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .manager import UserManager
from apps.common.models import BaseModel


class User(BaseModel ,AbstractBaseUser):
    class AuthStep(models.TextChoices):
        FIRST_STEP = "first step", "first step"
        SECOND_STEP = "second step", "second step"

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    auth_step = models.CharField(max_length=25, choices=AuthStep.choices, default=AuthStep.FIRST_STEP)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.full_name()
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    