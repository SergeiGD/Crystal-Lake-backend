from django.db import models
from django.urls import reverse

from ..offer.models import Offer, OfferQuerySet

# Create your models here.


class RoomQuerySet(OfferQuerySet):
    def search(self, **kwargs):
        qs = super().search(**kwargs)

        if kwargs.get('rooms', ''):
            qs = qs.filter(rooms=kwargs['rooms'])
        if kwargs.get('floors', ''):
            qs = qs.filter(floors=kwargs['floors'])
        if kwargs.get('beds', ''):
            qs = qs.filter(beds=kwargs['beds'])

        return qs


class Room(Offer):
    rooms = models.SmallIntegerField(verbose_name='комнат')
    floors = models.SmallIntegerField(verbose_name='этажей')
    beds = models.SmallIntegerField(verbose_name='спальных мест')
    square = models.FloatField(verbose_name='площадь')
    main_room = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name='номер представитель',
        related_name='child_rooms',
        related_query_name='child_room'
    )

    def get_absolute_url(self):
        return reverse('room', kwargs={'room_slug': self.slug})

    def get_admin_show_url(self):
        return reverse('admin_show_room', kwargs={'offer_id': self.pk})

    def get_admin_edit_url(self):
        return reverse('admin_edit_room', kwargs={'offer_id': self.pk})

    def get_admin_delete_url(self):
        return reverse('admin_delete_room', kwargs={'offer_id': self.pk})

    objects = RoomQuerySet.as_manager()
