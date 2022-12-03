import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
#from ..order.models import Purchase
from polymorphic.models import PolymorphicModel

# Create your models here.


class Offer(PolymorphicModel):
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
        indexes = [
            models.Index(fields=['date_deleted', 'is_hidden']),
            models.Index(fields=['slug'])
        ]

    def __str__(self):
        return self.name

    def get_main_photo(self):
        return self.photos.get(is_main=True).path.url


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


class Service(Offer):
    max_for_moment = models.SmallIntegerField(verbose_name="макс. единовременно")
    dynamic_timetable = models.BooleanField(verbose_name="динамическое расписание")


def build_photo_path(instance, filename):
    ext = filename.split('.')[-1]
    code = uuid.uuid4()
    return 'offer_{0}/{1}.{2}'.format(instance.offer.slug, code, ext)


class Photo(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="photos")
    is_main = models.BooleanField(default=False)
    order = models.SmallIntegerField()
    path = models.ImageField(upload_to=build_photo_path)




