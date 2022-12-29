from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from ..user.models import CustomUser
from ..service.models import Service

# Create your models here.


class Worker(CustomUser):
    qualifications = models.ManyToManyField(
        Service,
        related_name='workers',
        related_query_name='worker',
        blank=True
    )
    salary = models.DecimalField(
        verbose_name='зарплата',
        max_digits=12,
        decimal_places=2,
        blank=False,
        null=False
    )
    additional_info = models.TextField(
        verbose_name='доп. информация',
        null=False,
        blank=False
    )


    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = True

        super().save(*args, **kwargs)

    def get_admin_show_url(self):
        return reverse('admin_workers')

    def get_admin_edit_url(self):
        return reverse('admin_edit_worker', kwargs={'worker_id': self.pk})

    def get_admin_delete_url(self):
        return reverse('admin_delete_worker', kwargs={'worker_id': self.pk})




