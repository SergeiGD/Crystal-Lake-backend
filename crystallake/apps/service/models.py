from django.db import models
from django.urls import reverse

from ..offer.models import Offer

# Create your models here.


class Service(Offer):
    max_for_moment = models.SmallIntegerField(verbose_name='макс. единовременно')
    dynamic_timetable = models.BooleanField(verbose_name='динамическое расписание')

    def get_absolute_url(self):
        return reverse('service', kwargs={'service_slug': self.slug})

    def get_admin_show_url(self):
        return reverse('admin_show_service', kwargs={'offer_id': self.pk})

    def get_admin_delete_url(self):
        return reverse('admin_delete_service', kwargs={'offer_id': self.pk})

    def get_admin_edit_url(self):
        return reverse('admin_edit_service', kwargs={'offer_id': self.pk})

