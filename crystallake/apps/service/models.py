from datetimerange import DateTimeRange

from django.db import models
from django.urls import reverse
from django.utils.timezone import localtime
from django.db.models import Sum, Q

from ..offer.models import Offer
from ..offer.models import OfferQuerySet
from ..order.models import PurchaseCountable

# Create your models here.


class ServiceQuerySet(OfferQuerySet):
    def search(self, **kwargs):
        qs = super().search(**kwargs)
        if kwargs.get('max_in_group', ''):
            qs = qs.filter(max_in_group=kwargs['max_in_group'])
        # if kwargs.get('dynamic_timetable', ''):
        #     qs = qs.filter(dynamic_timetable=kwargs['dynamic_timetable'])

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
        if kwargs.get('sort_by', ''):
            qs = qs.order_by(kwargs['sort_by'])

        return qs


class Service(Offer):
    max_in_group = models.SmallIntegerField(verbose_name='макс. в группе', default=1)
    max_intersections = models.SmallIntegerField(verbose_name='макс пересечений', default=0)

    objects = ServiceQuerySet.as_manager()

    def get_info(self):
        data = super().get_info()
        data['max_in_group'] = self.max_in_group
        return data

    def get_free_time(self, start, end):
        result = []

        timetables = ServiceTimetable.objects.filter(
            service=self,
            start__gte=start,
            end__lte=end
        )

        # if self.dynamic_timetable:
        for timetable in timetables:
            result.append({
                'start': timetable.start.timestamp(),
                'end': timetable.end.timestamp(),
            })

        for timetable in timetables:
            purchases = PurchaseCountable.objects.filter(
                offer__pk=timetable.service.pk,
                is_canceled=False,
                order__date_canceled=None,
                start__gte=timetable.start,
                end__lte=timetable.start
            )

            time_ranges = []
            for purchase in purchases:
                time_range = DateTimeRange(purchase.start, purchase.end)
                time_ranges.append((time_range, purchase.quantity))

        # if not self.dynamic_timetable:
        #     for timetable in timetables:
        #
        #         purchases_count = PurchaseCountable.objects.filter(
        #             offer__pk=timetable.service.pk,
        #             is_canceled=False,
        #             order__date_canceled=None,
        #             start__gte=timetable.start,
        #             end__lte=timetable.end
        #         ).aggregate(total_quantity=Sum('quantity'))
        #
        #         if self.max_in_group == 0:
        #             result.append({
        #                 'start': timetable.start.timestamp(),
        #                 'end': timetable.end.timestamp(),
        #             })
        #         else:
        #             left = self.max_in_group if purchases_count['total_quantity'] is None else self.max_in_group - purchases_count['total_quantity']
        #
        #             if left > 0:
        #                 result.append({
        #                     'start': timetable.start.timestamp(),
        #                     'end': timetable.end.timestamp(),
        #                     'left': left
        #                 })

        return result

    def get_absolute_url(self):
        return reverse('service', kwargs={'service_slug': self.slug})

    def get_admin_show_url(self):
        return reverse('admin_show_service', kwargs={'offer_id': self.pk})

    def get_admin_delete_url(self):
        return reverse('admin_delete_service', kwargs={'offer_id': self.pk})

    def get_admin_edit_url(self):
        return reverse('admin_edit_service', kwargs={'offer_id': self.pk})

    def get_create_timetable_url(self):
        return reverse('create_timetable', kwargs={'offer_id': self.pk})

    def get_workers_url(self):
        return reverse('get_service_workers', kwargs={'offer_id': self.pk})

    def get_free_time_url(self):
        return reverse('get_free_time', kwargs={'offer_id': self.pk})

    def is_time_available(self, start, end):
        timetable = ServiceTimetable.objects.filter(
            service_id=self.pk,
            start__lte=start,
            end__gte=end
        ).first()

        if not timetable:
            return False

        purchases = PurchaseCountable.objects.filter(
            offer__id=self.pk,
            start__gte=timetable.start,
            end__lte=timetable.end,
            is_canceled=False,
            order__date_canceled=None
        )

        time_range = DateTimeRange(start, end)
        intersections_count = 0
        for purchase in purchases:
            if DateTimeRange(purchase.start, purchase.end).is_intersection(time_range):
                intersections_count += 1

        if intersections_count >= self.max_intersections:
            return False

        return True


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
            models.Index(fields=['start', 'end'])
        ]
        ordering = ['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_start = self.start
        self.__original_end = self.end

    # def get_purchases(self):
    #     return PurchaseCountable.objects.filter(
    #         start__gte=self.start,
    #         end__lte=self.end,
    #         is_canceled=False,
    #         order__date_canceled=None,
    #     )

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
            'edit_url': self.get_edit_url()
        }

    def get_info_url(self):
        return reverse('get_timetable', kwargs={'offer_id': self.service.pk, 'timetable_id': self.pk})

    def get_edit_url(self):
        return reverse('edit_timetable', kwargs={'offer_id': self.service.pk, 'timetable_id': self.pk})

    def get_delete_url(self):
        return reverse('delete_timetable',  kwargs={'offer_id': self.service.pk, 'timetable_id': self.pk})

