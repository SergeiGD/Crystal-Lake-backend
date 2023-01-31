from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

from .managers import CustomUserManager, SmsCodeManager

# Create your models here.


class CustomUser(AbstractUser):

    username = None

    GENDER_CHOICES = (
        ('male', 'мужской'),
        ('female', 'женский'),
        ('unknown', 'не выбрано'),
    )

    phone = PhoneNumberField(
        null=False,
        blank=False,
        unique=True,
        region='RU',
        verbose_name='Номер телефона'
    )
    gender = models.CharField(
        max_length=50,
        choices=GENDER_CHOICES,
        blank=False,
        null=False,
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
        if not self.first_name and not self.last_name:
            return 'Неизвестно'
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return self.full_name

    def mark_as_deleted(self):
        self.date_deleted = timezone.now()
        self.last_name = self.last_name + '-DELETED'
        self.save()


class SmsCode(models.Model):
    phone = PhoneNumberField(
        null=False,
        blank=False,
        unique=False,
        region='RU',
        verbose_name='Номер телефона'
    )
    date = models.DateTimeField(
        null=False,
        blank=False,
        unique=False,
        verbose_name='Время отправки'
    )
    code = models.TextField(
        null=False,
        blank=False,
        unique=False,
        verbose_name='Код'
    )
    is_used = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name='Использован'
    )

    objects = SmsCodeManager()
