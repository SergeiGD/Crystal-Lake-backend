from django.db import models
from django.urls import reverse

from ..user.models import CustomUser

# Create your models here.


class Client(CustomUser):
    bonuses = models.IntegerField(verbose_name='Бонусов', blank=True, default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = False

        super().save(*args, **kwargs)

    def get_admin_show_url(self):
        return reverse('admin_clients')



