from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractUser):
    phone = PhoneNumberField(null=False, blank=False, unique=True, region='RU', verbose_name='Номер телефона')
    username = None

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['phone']
