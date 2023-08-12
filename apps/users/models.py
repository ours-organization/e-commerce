import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .manager import UserManager


class BaseModel(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel ,AbstractBaseUser):
    class UserAddress(models.TextChoices):
        TASHKENT = "tashkent", "tashkent"
        TOSHKENT_REG = "tashkent reg", "tashkent reg"
        ANDIJON = "andijan", "andijan"
        NAMANGAN = "namangan", "namangan"
        FARGONA = "fergana", "fergana"
        SIRDARIO = "sirdarya", "sirdarya"
        JIZZAKH = "jizzakh", "jizzakh"
        SAMARKAND = "samarkand", "samarkand"
        SURKHANDARYA = "surkhandarya", "surkhandarya"
        KASHKADARYA = "kashkadarya", "kashkadarya"
        NAVOIY = "navoiy", "navoiy"
        BUKHARA = "bukhara", "bukhara"
        KHAREZM = "kharezm", "kharezm"
        KARAKALPAKISTAN = "karakalpakistan", "karakalpakistan"

    class AuthStep(models.TextChoices):
        FIRST_STEP = "first step", "first step"
        SECOND_STEP = "second step", "second step"

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=25, choices=UserAddress.choices, default=UserAddress.TASHKENT)
    auth_step = models.CharField(max_length=25, choices=AuthStep.choices, default=AuthStep.FIRST_STEP)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name()
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []