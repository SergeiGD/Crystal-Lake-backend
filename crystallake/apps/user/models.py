from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractUser):

    username = None
    GENDER_CHOISES = (
        ('male', 'мужской'),
        ('female', 'женский'),
        ('unknown', 'не выбрано'),
    )

    phone = PhoneNumberField(
        null=False, blank=False,
        unique=True, region='RU',
        verbose_name='Номер телефона'
    )
    gender = models.CharField(
        max_length=50, choices=GENDER_CHOISES,
        blank=False, null=False,
        verbose_name='Пол',
        default='unknown'
    )
    date_deleted = models.DateTimeField(
        verbose_name='дата удаления',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return self.full_name

    def mark_as_deleted(self):
        self.date_deleted = timezone.now()
        self.last_name = self.last_name + '-DELETED'
        self.save()

