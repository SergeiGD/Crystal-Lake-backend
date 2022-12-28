import copy

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
    rooms = models.SmallIntegerField(verbose_name='комнат', null=True)
    floors = models.SmallIntegerField(verbose_name='этажей', null=True)
    beds = models.SmallIntegerField(verbose_name='спальных мест', null=True)
    square = models.FloatField(verbose_name='площадь', null=True)
    main_room = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name='номер представитель',
        related_name='child_rooms',
        related_query_name='child_room'
    )

    def create_same_room(self):
        if self.main_room is not None:
            raise ValueError('Нельзя создать копию номера, который сам является копией')

        same_room = Room(main_room=self)
        same_room.copy_parent_fields()
        same_room.save()
        return same_room

    def copy_parent_fields(self):
        if self.main_room is None:
            raise ValueError('Комната не имеет родительскую комнату')
        self.is_hidden = True
        self.name = self.main_room.name
        self.default_price = self.main_room.default_price
        self.weekend_price = self.main_room.weekend_price
        self.prepayment_percent = self.main_room.prepayment_percent
        self.refund_percent = self.main_room.refund_percent

    def get_same_rooms(self):
        return Room.objects.filter(date_deleted=None, main_room=self)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for room in self.get_same_rooms():
            room.copy_parent_fields()
            room.save()

    def get_absolute_url(self):
        if self.main_room is None:
            return reverse('room', kwargs={'room_slug': self.slug})
        return reverse('room', kwargs={'room_slug': self.main_room.slug})

    def get_admin_show_url(self):
        if self.main_room is None:
            return reverse('admin_show_room', kwargs={'offer_id': self.pk})
        return reverse('admin_show_room', kwargs={'offer_id': self.main_room.pk})

    def get_admin_edit_url(self):
        if self.main_room is None:
            return reverse('admin_edit_room', kwargs={'offer_id': self.pk})
        return reverse('admin_edit_room', kwargs={'offer_id': self.main_room.pk})

    def get_admin_delete_url(self):
        return reverse('admin_delete_room', kwargs={'offer_id': self.pk})

    def get_create_same_room_url(self):
        return reverse('create_same_room', kwargs={'offer_id': self.pk})

    def get_del_same_room_url(self):
        return reverse('del_same_room', kwargs={'offer_id': self.pk})

    objects = RoomQuerySet.as_manager()
