from datetimerange import DateTimeRange
from datetime import timedelta, datetime, time, date

from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.timezone import localtime, make_aware

from ..offer.models import Offer, OfferQuerySet
from ..order.models import Purchase
from django.conf import settings

# Create your models here.


class RoomQuerySet(OfferQuerySet):
    def get_free_rooms(self, start, end):
        rooms = self.filter(
            is_hidden=False,
            date_deleted=None,
            main_room=None
        )
        result = []
        for room in rooms:
            busy_dates = room.get_general_busy_dates(start, end)
            if len(busy_dates) == 0:
                result.append(room)

        rooms_ids = [room.id for room in result]
        queryset = rooms.filter(id__in=rooms_ids)

        return queryset

    def search(self, **kwargs):
        qs = super().search(**kwargs)

        if kwargs.get('rooms', ''):
            qs = qs.filter(rooms=kwargs['rooms'])
        if kwargs.get('floors', ''):
            qs = qs.filter(floors=kwargs['floors'])
        if kwargs.get('beds', ''):
            qs = qs.filter(beds=kwargs['beds'])
        if kwargs.get('beds_from', ''):
            qs = qs.filter(beds__gte=kwargs['beds_from'])
        if kwargs.get('beds_until', ''):
            qs = qs.filter(beds__lte=kwargs['beds_until'])
        if kwargs.get('rooms_from', ''):
            qs = qs.filter(rooms__gte=kwargs['rooms_from'])
        if kwargs.get('rooms_until', ''):
            qs = qs.filter(rooms__lte=kwargs['rooms_until'])
        if kwargs.get('dates_from', '') and kwargs.get('dates_until', ''):
            if isinstance(kwargs['dates_from'], date):
                dates_from = datetime.combine(kwargs['dates_from'], settings.CHECK_IN_TIME)
                dates_until = datetime.combine(kwargs['dates_until'], settings.CHECK_IN_TIME)
            else:
                dates_from = datetime.strptime(kwargs['dates_from'], "%Y-%m-%d")
                dates_until = datetime.strptime(kwargs['dates_until'], "%Y-%m-%d")
            start, end = make_aware(dates_from), make_aware(dates_until)
            qs = qs.get_free_rooms(start, end)

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

    def get_main_photo(self):
        if self.main_room is None:
            return super().get_main_photo()
        return self.main_room.get_main_photo()

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
        self.prepayment_percent = self.main_room.prepayment_percent
        self.refund_percent = self.main_room.refund_percent

    def get_same_rooms(self):
        return Room.objects.filter(date_deleted=None, main_room=self)

    def pick_rooms_for_purchase(self, start, end, purchase_id=None):
        result = []

        while start != end:
            rooms_dates = {}
            dates_range = DateTimeRange(start, end - timedelta(days=1))
            for room in self.get_same_rooms():
                rooms_dates[room] = 0
                for date in dates_range.range(timedelta(days=1)):
                    if not room.is_day_busy(date, purchase_id):
                        rooms_dates[room] += 1
                    else:
                        break
            max_room_delta = max(rooms_dates.items(), key=lambda pair: pair[1])
            room = max_room_delta[0]
            room_start = start
            room_end = start + timedelta(days=max_room_delta[1])
            result.append({
                'room': room,
                'start': room_start,
                'end': datetime.combine(room_end.date(), settings.CHECK_OUT_TIME)
            })
            start = room_end
            if max_room_delta[1] == 0:
                return []

        return result

    def is_day_busy(self, day, purchase_id=None):

        return Purchase.objects.exclude(pk=purchase_id).filter(
                offer__pk=self.pk,
                is_canceled=False,
                order__date_canceled=None,
                start__lte=day,
                end__gte=day,
            ).exists()

    def get_general_busy_dates(self, start, end):
        general_dates = []
        room = self if self.main_room is None else self.main_room

        rooms = room.get_same_rooms()

        if len(rooms) == 1:
            return rooms[0].get_busy_dates(start, end)

        for same_room in rooms:
            room_dates = set()

            purchases = Purchase.objects.filter(
                Q(start__range=[start, end]) | Q(end__range=[start, end]),
                offer__pk=same_room.pk,
                is_canceled=False,
                order__date_canceled=None,
            )

            for purchase in purchases:
                dates_range = DateTimeRange(purchase.start, purchase.end)
                for date in dates_range.range(timedelta(days=1)):
                    room_dates.add(date.timestamp())

            general_dates.append(room_dates)

        if len(general_dates) > 1:
            result = set.intersection(*general_dates)
            return list(result)

        return []

    def get_busy_dates(self, start, end):
        dates = set()

        if self.main_room is not None:

            purchases = Purchase.objects.filter(
                Q(start__range=[start, end]) | Q(end__range=[start, end]),
                offer__pk=self.pk,
                is_canceled=False,
                order__date_canceled=None,
            )

            for purchase in purchases:
                dates_range = DateTimeRange(purchase.start, purchase.end)
                for date in dates_range.range(timedelta(days=1)):
                    dates.add(date.timestamp())
        else:
            raise ValueError('Нельзя получить конкретное расписание родительской комнаты')
        return list(dates)

    def get_info(self):
        data = super().get_info()
        data['link'] = self.get_admin_show_url()
        data['rooms'] = self.rooms
        data['floors'] = self.floors
        data['beds'] = self.floors
        data['square'] = self.square
        return data

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

    def get_busy_dates_url(self):
        return reverse('get_busy_dates', kwargs={'offer_id': self.main_room.pk, 'room_id': self.pk})

    def get_general_busy_dates_url(self):
        return reverse('get_general_busy_dates', kwargs={'offer_id': self.pk})

    objects = RoomQuerySet.as_manager()
