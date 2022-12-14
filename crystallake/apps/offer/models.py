import itertools
import uuid
import base64

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from pytils.translit import slugify
#from django.utils.text import slugify
#from ..order.models import Purchase
from polymorphic.models import PolymorphicModel

# Create your models here.


def build_photo_path(instance, filename):
    """
    генерация пути для фотографий
    """
    ext = filename.split('.')[-1]
    code = uuid.uuid4()
    if hasattr(instance, 'offer'):      # если дополнительная фотография, то берем id из оффера
        return 'offer_{0}/{1}.{2}'.format(instance.offer.pk, code, ext)

    return 'offer_{0}/{1}.{2}'.format(instance.pk, code, ext)


class Offer(PolymorphicModel):
    name = models.CharField(verbose_name="наименование", max_length=255, unique=True)
    description = models.TextField(verbose_name="описание")
    default_price = models.DecimalField(verbose_name="стандартная цена", max_digits=12, decimal_places=2)
    weekend_price = models.DecimalField(verbose_name="праздничная цена", max_digits=12, decimal_places=2, )
    prepayment_percent = models.FloatField(verbose_name="предоплата")
    refund_percent = models.FloatField(verbose_name="возврат")
    main_photo = models.ImageField(upload_to=build_photo_path)
    date_create = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    date_deleted = models.DateTimeField(verbose_name="дата удаления", blank=True, null=True)
    is_hidden = models.BooleanField(verbose_name="скрыто", default=False)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['date_deleted', 'is_hidden']),
            models.Index(fields=['slug'])
        ]
        ordering = ['date_create']

    def __str__(self):
        return self.name

    def get_orders_count(self):
        pass

    def _generate_slug(self):
        """
        автоматичекая генерация слага
        """
        value = self.name
        slug_candidate = slug_original = slugify(value)
        for i in itertools.count(1):
            if not Offer.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)           # если слаг занят, то добавлем цифру в конце

        self.slug = slug_candidate

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_name = self.name                    # сохраняем изначальное имя, на случай, если его изменяет

    def save(self, *args, **kwargs):
        if not self.pk or self.__original_name != self.name:    # если новый объект или сменили имя, то генерируем слаг
            self._generate_slug()

        super().save(*args, **kwargs)


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

    def get_absolute_url(self):
        return reverse('room', kwargs={'room_slug': self.slug})

    def get_admin_show_url(self):
        return reverse('admin_show_room', kwargs={'room_slug': self.slug})

    def get_admin_edit_url(self):
        return reverse('admin_edit_room', kwargs={'room_slug': self.slug})


class Service(Offer):
    max_for_moment = models.SmallIntegerField(verbose_name="макс. единовременно")
    dynamic_timetable = models.BooleanField(verbose_name="динамическое расписание")


class Photo(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="photos")
    order = models.SmallIntegerField()
    path = models.ImageField(upload_to=build_photo_path)

    class Meta:
        ordering = ['order']

    def get_base64(self):
        base64_str = base64.b64encode(self.path.read()).decode('utf-8')
        ext = self.path.url.split('.')[-1]
        return f'data:image/{ext};base64,{base64_str}'
        # with open(self.path.url, 'rb') as image:
        #     return base64.b64encode(image.read())




