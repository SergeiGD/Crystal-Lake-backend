# import datetime
from datetime import timedelta, time, date, datetime

from datetimerange import DateTimeRange

from django.db import models
from django.urls import reverse
from django.utils.timezone import localtime, make_aware
from django.db.models import Sum, Q

from ..offer.models import Offer
from ..offer.models import OfferQuerySet
from ..order.models import PurchaseCountable

# Create your models here.


# class ServiceQuerySet(OfferQuerySet):
#     def search(self, **kwargs):
#         qs = super().search(**kwargs)
#         if kwargs.get('max_in_group', ''):
#             qs = qs.filter(max_in_group=kwargs['max_in_group'])
#
#         return qs


class ServiceQuerySet(OfferQuerySet):
    def get_free_services(self, start, end):
        services = self.filter(
            is_hidden=False,
            date_deleted=None,
        )
        result = []
        for service in services:
            if service.is_time_available(start, end):
                result.append(service)

        services_ids = [service.id for service in result]
        queryset = services.filter(id__in=services_ids)

        return queryset

    def search(self, **kwargs):
        qs = super().search(**kwargs)

        if kwargs.get('max_in_group', ''):
            qs = qs.filter(max_in_group=kwargs['max_in_group'])
        if kwargs.get('dates_from', '') and kwargs.get('time_from', '') and kwargs.get('time_until', ''):
            if isinstance(kwargs['dates_from'], date):
                dates_from = datetime.combine(kwargs['dates_from'], kwargs['time_from'])
                dates_until = datetime.combine(kwargs['dates_from'],  kwargs['time_until'])
            else:
                dates_from = datetime.strptime(f'{kwargs["dates_from"]} {kwargs["time_from"]}', "%Y-%m-%d %H:%M")
                dates_until = datetime.strptime(f'{kwargs["dates_from"]} {kwargs["time_until"]}', "%Y-%m-%d %H:%M")
            start, end = make_aware(dates_from), make_aware(dates_until)
            qs = qs.get_free_services(start, end)

        return qs


class ServiceTimetableQuerySet(models.QuerySet):
    def search(self, **kwargs):
        qs = self
        if kwargs.get('service_id', ''):
            qs = qs.filter(service__id=kwargs['service_id'])
        if kwargs.get('start', ''):
            qs = qs.filter(start__gte=kwargs['start'])
        if kwargs.get('end', ''):
            qs = qs.filter(end__lte=kwargs['end'])

        return qs


class Service(Offer):
    max_in_group = models.SmallIntegerField(verbose_name='макс. в группе', default=1)
    max_intersections = models.SmallIntegerField(verbose_name='макс пересечений', default=0)
    min_time = models.SmallIntegerField(verbose_name='мин. время брони', default=30, null=False, blank=False)

    objects = ServiceQuerySet.as_manager()

    def get_info(self):
        data = super().get_info()
        data['max_in_group'] = self.max_in_group
        return data

    def get_free_time(self, start, end):
        result = []

        timetables = ServiceTimetable.objects.filter(
            service_id=self.pk,
            start__gte=start,
            end__lte=end
        )

        for timetable in timetables:
            current_time = timetable.start
            step = timedelta(minutes=10)
            banned_ranges = []

            while current_time < timetable.end:
                time_range = DateTimeRange(current_time, current_time + step)

                if PurchaseCountable.objects.filter(
                    Q(start__range=[current_time, current_time + step]) |
                    Q(end__range=[current_time, current_time + step]) |
                    (Q(start__lte=current_time) & Q(end__gte=current_time + step)),
                    offer__pk=timetable.service.pk,
                    is_canceled=False,
                    order__date_canceled=None,
                ).count() >= self.max_intersections:
                    banned_ranges.append(time_range)

                current_time += step

            available_ranges = [DateTimeRange(timetable.start, timetable.end)]      # изначально доступно все время расписания
            for banned_time in banned_ranges:
                temp = []
                for available_time in available_ranges:
                    timetable_range = available_time.subtract(banned_time)          # отнимаем от текущего диапозона запрещенный диапозон
                    temp.extend(timetable_range)
                available_ranges = temp

            for available_time in available_ranges:
                result.append({
                    'start': available_time.start_datetime.timestamp(),             # возращаем в виде таймстемпов
                    'end': available_time.end_datetime.timestamp(),
                })

        return result

    def is_time_available(self, start, end, purchase_id=None):
        timetable = ServiceTimetable.objects.filter(
            service_id=self.pk,
            start__lte=start,
            end__gte=end
        ).first()

        if not timetable:
            return False

        purchases = PurchaseCountable.objects.exclude(pk=purchase_id).filter(
            offer__id=self.pk,
            start__gte=timetable.start,
            end__lte=timetable.end,
            is_canceled=False,
            order__date_canceled=None
        )

        time_range = DateTimeRange(start, end)
        intersections_count = 0
        for purchase in purchases:
            purchase_start = purchase.start + timedelta(seconds=5)     # прибавим от отнимем по 5 сек, чтоб если одна запись встает на конец/начало
            purchase_end = purchase.end - timedelta(seconds=5)         # другой, мы не считали это за пересечение
            if DateTimeRange(purchase_start, purchase_end).is_intersection(time_range):
                intersections_count += 1

        if intersections_count >= self.max_intersections:
            return False

        return True

    def get_absolute_url(self):
        return reverse('service', kwargs={'service_slug': self.slug})

    def get_admin_show_url(self):
        return reverse('admin_show_service', kwargs={'offer_id': self.pk})

    def get_admin_delete_url(self):
        return reverse('admin_delete_service', kwargs={'offer_id': self.pk})

    def get_admin_edit_url(self):
        return reverse('admin_edit_service', kwargs={'offer_id': self.pk})

    def get_timetables_url(self):
        return reverse('admin_service_timetables', kwargs={'offer_id': self.pk})

    def get_create_timetable_url(self):
        return reverse('create_timetable', kwargs={'offer_id': self.pk})

    def get_workers_url(self):
        return reverse('get_service_workers', kwargs={'offer_id': self.pk})

    def get_free_time_url(self):
        return reverse('get_free_time', kwargs={'offer_id': self.pk})

    def get_edit_timetable_url(self):
        return reverse('edit_timetable', kwargs={'offer_id': self.service.pk})

    def get_delete_timetable_url(self):
        return reverse('delete_timetable',  kwargs={'offer_id': self.service.pk})


class ServiceTimetable(models.Model):
    service = models.ForeignKey(
        Service,
        verbose_name='услуга',
        related_name='timetables',
        related_query_name='timetable',
        on_delete=models.CASCADE
    )
    start = models.DateTimeField(verbose_name='Начало')
    end = models.DateTimeField(verbose_name='Конце')
    workers = models.ManyToManyField(
        'worker.Worker',
        verbose_name='Сотрудники',
        related_name='timetables',
        related_query_name='timetable'
    )

    objects = ServiceTimetableQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=['service_id', 'start', 'end'])
        ]
        ordering = ['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_start = self.start
        self.__original_end = self.end

    def save(self, *args, **kwargs):
        self.clean()

        super().save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError

        purchases_original_time = PurchaseCountable.objects.none()

        if self.pk:
            purchases_original_time = PurchaseCountable.objects.filter(
                start__gte=self.__original_start,
                end__lte=self.__original_end,
                offer__pk=self.service.pk,
                is_canceled=False,
                order__date_canceled=None,
            )

        if self.pk and purchases_original_time.filter(Q(start__lt=self.start) | Q(end__gt=self.end)).exists():
            raise ValidationError('Выбор данного времени приведет к невозможности оказать услуги')

        intersections = ServiceTimetable.objects.filter(
            service_id=self.service.id,
            start__year=self.start.year,
            start__month=self.start.month,
            start__day=self.start.day
        ).exclude(pk=self.pk)
        for intersection in intersections:
            time_range = DateTimeRange(intersection.start, intersection.end)
            if DateTimeRange(self.start, self.end).is_intersection(time_range):
                raise ValidationError('На это время уже есть расписание')

    def get_purchases(self):
        return PurchaseCountable.objects.filter(
            start__gte=self.start,
            end__lte=self.end,
            offer__pk=self.service.pk,
            is_canceled=False,
            order__date_canceled=None,
        )

    def get_info(self):
        workers = []
        for worker in self.workers.all():
            workers.append({
                'id': worker.pk,
                'name': worker.full_name,
                'link': worker.get_admin_show_url(),
                'phone': worker.phone
            })

        return {
            'start': self.start.timestamp(),
            'end': self.end.timestamp(),
            'id': self.pk,
            'workers': workers,
            'edit_url': self.service.get_edit_timetable_url()
        }

    def get_info_url(self):
        return reverse('get_timetable', kwargs={'offer_id': self.service.pk, 'timetable_id': self.pk})

    # def get_edit_url(self):
    #     return reverse('edit_timetable', kwargs={'offer_id': self.service.pk, 'timetable_id': self.pk})
    #
    # def get_delete_url(self):
    #     return reverse('delete_timetable',  kwargs={'offer_id': self.service.pk, 'timetable_id': self.pk})

