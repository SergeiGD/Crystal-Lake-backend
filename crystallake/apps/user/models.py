from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.urls import reverse

from .managers import CustomUserManager, SmsCodeManager
from ..order.models import Order
from .code_type_choises import CODE_TYPE_CHOICES

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

    def get_cart(self):
        return Order.objects.filter(
            client=self,
            paid=0, refunded=0,
            date_canceled=None,
            date_finished=None
        ).first()

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return self.full_name

    def mark_as_deleted(self):
        self.date_deleted = timezone.now()
        self.last_name = self.last_name + '-DELETED'
        self.save()

    def get_admin_show_url(self):
        if self.is_staff:
            return reverse('admin_show_worker', kwargs={'worker_id': self.pk})
        return reverse('admin_show_client', kwargs={'client_id': self.pk})


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
    ip = models.CharField(
        null=False,
        blank=False,
        verbose_name='ip',
        max_length=30
    )
    type = models.CharField(
        choices=CODE_TYPE_CHOICES,
        null=False,
        blank=False,
        default='register',
        verbose_name='Тип запроса',
        max_length=50
    )

    objects = SmsCodeManager()
