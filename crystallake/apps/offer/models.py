from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from ..order.models import Purchase

# Create your models here.


class Offer(models.Model):
    name = models.CharField(verbose_name="наименование", max_length=255)
    description = models.TextField(verbose_name="описание")
    default_price = models.DecimalField(verbose_name="стандартная цена", max_digits=12, decimal_places=5)
    weekend_price = models.DecimalField(verbose_name="цена по праздникам", max_digits=12, decimal_places=5)
    prepayment_percent = models.FloatField(verbose_name="предоплата")
    refund_percent = models.FloatField(verbose_name="возврат")
    date_create = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    date_deleted = models.DateTimeField(verbose_name="дата удаления", blank=True, null=True)
    is_hidden = models.BooleanField(verbose_name="скрыто", default=False)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['date_deleted', 'is_hidden']),
            models.Index(fields=['slug'])
        ]

    def __str__(self):
        return self.name


class Room(Offer):
    rooms = models.SmallIntegerField(verbose_name="комнат")
    floors = models.SmallIntegerField(verbose_name="этажей")
    beds = models.SmallIntegerField(verbose_name="спальных мест")
    square = models.FloatField(verbose_name="площадь")
    main_room = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="номер представитель",
        related_name="child_rooms",
        related_query_name="child_room"
    )


    orders = GenericRelation(Purchase, related_name="rooms", related_query_name="room")


class Service(Offer):
    max_for_moment = models.SmallIntegerField(verbose_name="макс. единовременно")
    dynamic_timetable = models.BooleanField(verbose_name="динамическое расписание")
    orders = GenericRelation(Purchase, related_name="services", related_query_name="service")

