import datetime
import itertools
from pytils.translit import slugify

from django.db import models
from django.urls import reverse
from django.utils import timezone

from polymorphic.models import PolymorphicModel
from polymorphic.query import PolymorphicQuerySet

from ..tag.models import Tag
from ..core.build_photo_path import build_photo_path
from .price_choises import PRICE_CHOICES

# Create your models here.


class OfferQuerySet(PolymorphicQuerySet):
    def search(self, **kwargs):
        qs = self
        if kwargs.get('id', ''):
            qs = qs.filter(id=kwargs['id'])
        if kwargs.get('name', ''):
            qs = qs.filter(name__icontains=kwargs['name'])
        if kwargs.get('price_from', ''):
            qs = qs.filter(default_price__gte=kwargs['price_from'])
        if kwargs.get('price_until', ''):
            qs = qs.filter(default_price__lte=kwargs['price_until'])
        if kwargs.get('weekend_price_from', ''):
            qs = qs.filter(weekend_price__gte=kwargs['weekend_price_from'])
        if kwargs.get('weekend_price_until', ''):
            qs = qs.filter(weekend_price__lte=kwargs['weekend_price_until'])
        if kwargs.get('sort_by', ''):
            qs = qs.order_by(kwargs['sort_by'])

        return qs


class Offer(PolymorphicModel):
    # PRICE_CHOICES = (
    #     ('hours', 'часы'),
    #     ('days', 'дни'),
    # )

    name = models.CharField(
        verbose_name='наименование',
        max_length=255,
        blank=False,
        null=False
    )
    description = models.TextField(
        verbose_name='описание',
        blank=False,
        null=True
    )
    price_type = models.CharField(
        max_length=50, choices=PRICE_CHOICES,
        blank=False, null=False,
        verbose_name='Цена за',
        default='day',
    )
    default_price = models.DecimalField(
        verbose_name='стандартная цена',
        max_digits=12,
        decimal_places=2,
        blank=False,
        null=False
    )
    weekend_price = models.DecimalField(
        verbose_name='праздничная цена',
        max_digits=12,
        decimal_places=2,
        blank=False,
        null=False
    )
    prepayment_percent = models.FloatField(
        verbose_name='предоплата',
        blank=False,
        null=False
    )
    refund_percent = models.FloatField(
        verbose_name='возврат',
        blank=False,
        null=False
    )
    main_photo = models.ImageField(
        upload_to=build_photo_path,
        blank=False,
        null=True,
        db_column='main_photo'
    )

    def get_main_photo(self):
        return self.main_photo

    date_create = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True,
        blank=False,
        null=False
    )
    date_deleted = models.DateTimeField(
        verbose_name='дата удаления',
        blank=True,
        null=True
    )
    is_hidden = models.BooleanField(
        verbose_name='скрыто',
        default=False,
        blank=False,
        null=False
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=False,
        null=False
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='offers',
        related_query_name='offer',
        blank=True
    )

    objects = OfferQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=['date_deleted', 'is_hidden']),
            models.Index(fields=['slug'])
        ]
        ordering = ['date_create']

    def __str__(self):
        return self.name

    def get_info(self):
        return {
            'name': self.name,
            'id': self.pk,
            'default_price': self.pk,
            'is_hidden': self.is_hidden,
        }

    def get_familiar(self):
        tags_intersection = {}
        for i in self.__class__.objects.filter(date_deleted=None, is_hidden=False):
            tags_intersection[i] = len(self.tags.all() & i.tags.all())

        sorted_familiar = [k for k, v in sorted(tags_intersection.items(), key=lambda item: item[1], reverse=True)]
        return sorted_familiar[0:3]

    def mark_as_deleted(self):
        self.date_deleted = timezone.now()
        # self.name = self.name + '-DELETED'
        self.save()

    def get_add_tag_url(self):
        return reverse('add_tag_to_offer', kwargs={'offer_id': self.pk})

    def get_del_tag_url(self):
        return reverse('del_tag_from_offer', kwargs={'offer_id': self.pk})

    def get_tags_url(self):
        return reverse('get_tags_for_offer', kwargs={'offer_id': self.pk})

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





