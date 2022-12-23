from django.db import models

from ..offer.models import Offer

# Create your models here.


class Service(Offer):
    max_for_moment = models.SmallIntegerField(verbose_name='макс. единовременно')
    dynamic_timetable = models.BooleanField(verbose_name='динамическое расписание')
