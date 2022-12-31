from django.db import models
from django.urls import reverse

from ..offer.models import Offer
from ..offer.models import OfferQuerySet

# Create your models here.


class ServiceQuerySet(OfferQuerySet):
    def search(self, **kwargs):
        qs = super().search(**kwargs)
        if kwargs.get('max_for_moment', ''):
            qs = qs.filter(max_for_moment=kwargs['max_for_moment'])
        if kwargs.get('dynamic_timetable', ''):
            qs = qs.filter(dynamic_timetable=kwargs['dynamic_timetable'])

        return qs

class Service(Offer):
    max_for_moment = models.SmallIntegerField(verbose_name='макс. единовременно')
    dynamic_timetable = models.BooleanField(verbose_name='динамическое расписание')

    objects = ServiceQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('service', kwargs={'service_slug': self.slug})

    def get_admin_show_url(self):
        return reverse('admin_show_service', kwargs={'offer_id': self.pk})

    def get_admin_delete_url(self):
        return reverse('admin_delete_service', kwargs={'offer_id': self.pk})

    def get_admin_edit_url(self):
        return reverse('admin_edit_service', kwargs={'offer_id': self.pk})

