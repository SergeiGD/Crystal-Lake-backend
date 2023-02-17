from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.db.models import Sum

from ..user.models import CustomUser
from ..order.models import Order

# Create your models here.


class Client(CustomUser):
    # TODO: сделать прокси
    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = False

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id']

    def get_orders_count(self):
        return Order.objects.filter(client=self, date_canceled=None).count()

    def get_money_spent(self):
        spent = Order.objects.filter(client=self, date_canceled=None).aggregate(Sum('paid'))['paid__sum']
        if spent:
            return spent
        return 0

    def get_admin_show_url(self):
        return reverse('admin_show_client', kwargs={'client_id': self.pk})

    def get_admin_edit_url(self):
        return reverse('admin_edit_client', kwargs={'client_id': self.pk})



