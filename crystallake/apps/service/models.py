from datetimerange import DateTimeRange

from django.db import models
from django.urls import reverse
from django.utils.timezone import localtime
from django.db.models import Sum

from ..offer.models import Offer
from ..offer.models import OfferQuerySet
from ..order.models import PurchaseCountable

# Create your models here.


class ServiceQuerySet(OfferQuerySet):
    def search(self, **kwargs):
        qs = super().search(**kwargs)
        if kwargs.get('max_in_group', ''):
            qs = qs.filter(max_in_group=kwargs['max_in_group'])
        if kwargs.get('dynamic_timetable', ''):
            qs = qs.filter(dynamic_timetable=kwargs['dynamic_timetable'])

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
    dynamic_timetable = models.BooleanField(verbose_name='динамическое расписание')

    objects = ServiceQuerySet.as_manager()

    def get_info(self):
        data = super().get_info()
        data['max_in_group'] = self.max_in_group
        data['dynamic_timetable'] = self.dynamic_timetable
        return data

    def get_free_time(self, start, end):
        result = []

        timetables = ServiceTimetable.objects.filter(
            service=self,
            start__gte=start,
            end__lte=end
        )

        if self.dynamic_timetable:
            for timetable in timetables:
                result.append({
                    'start': timetable.start.timestamp(),
                    'end': timetable.end.timestamp(),
                })

            # for timetable in timetables:
            #     purchases = PurchaseCountable.objects.filter(
            #         offer__pk=timetable.service.pk,
            #         is_canceled=False,
            #         order__date_canceled=None,
            #         start__gte=timetable.start,
            #         end__lte=timetable.start
            #     )
            #
            #     time_ranges = []
            #     for purchase in purchases:
            #         time_range = DateTimeRange(purchase.start, purchase.end)
            #         time_ranges.append((time_range, purchase.quantity))

        if not self.dynamic_timetable:
            for timetable in timetables:

                purchases_count = PurchaseCountable.objects.filter(
                    offer__pk=timetable.service.pk,
                    is_canceled=False,
                    order__date_canceled=None,
                    start__gte=timetable.start,
                    end__lte=timetable.end
                ).aggregate(total_quantity=Sum('quantity'))

                if self.max_in_group == 0:
                    result.append({
                        'start': timetable.start.timestamp(),
                        'end': timetable.end.timestamp(),
                    })
                else:
                    left = self.max_in_group if purchases_count['total_quantity'] is None else self.max_in_group - purchases_count['total_quantity']

                    if left > 0:
                        result.append({
                            'start': timetable.start.timestamp(),
                            'end': timetable.end.timestamp(),
                            'left': left
                        })

        print(result)
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

    def get_edit_timetable_url(self):
        pass

    def get_delete_timetable_url(self):
        pass

    def get_workers_url(self):
        return reverse('get_service_workers', kwargs={'offer_id': self.pk})

    def get_free_time_url(self):
        return reverse('get_free_time', kwargs={'offer_id': self.pk})


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
            'workers': workers
        }

    def get_info_url(self):
        return reverse('get_timetable', kwargs={'offer_id': self.service.pk, 'timetable_id': self.pk})

