from django.db import models
from django.urls import reverse

from ..user.models import CustomUser
from ..service.models import Service

from ..user.managers import UserQuerySet, CustomUserManager

# Create your models here.


class WorkerQuerySet(UserQuerySet):
    """
    Кверисет для удобного поиска по данным с форм
    """
    def search(self, **kwargs):
        qs = super().search(**kwargs)
        if kwargs.get('offer_id', ''):
            qs = qs.filter(qualifications__pk__in=[kwargs['offer_id']])

        return qs


class WorkerManager(CustomUserManager):
    def get_queryset(self):
        return WorkerQuerySet(self.model, self._db)       # использем расширенный кверисет с методом search


class Worker(CustomUser):
    qualifications = models.ManyToManyField(
        Service,
        related_name='workers',
        related_query_name='worker',
        blank=True
    )
    salary = models.DecimalField(
        verbose_name='зарплата',
        max_digits=12,
        decimal_places=2,
        blank=False,
        null=False
    )
    additional_info = models.TextField(
        verbose_name='доп. информация',
        null=True,
        blank=True
    )

    objects = WorkerManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = True

        super().save(*args, **kwargs)

    def get_admin_show_url(self):
        return reverse('admin_show_worker', kwargs={'worker_id': self.pk})

    def get_admin_edit_url(self):
        return reverse('admin_edit_worker', kwargs={'worker_id': self.pk})

    def get_admin_delete_url(self):
        return reverse('admin_delete_worker', kwargs={'worker_id': self.pk})

    def get_services_url(self):
        return reverse('get_services_for_worker', kwargs={'worker_id': self.pk})

    def get_add_service_url(self):
        return reverse('add_service_to_worker', kwargs={'worker_id': self.pk})

    def get_del_service_url(self):
        return reverse('del_service_from_worker', kwargs={'worker_id': self.pk})

    def get_groups_url(self):
        return reverse('get_groups_for_worker', kwargs={'worker_id': self.pk})

    def get_add_group_url(self):
        return reverse('add_group_to_worker', kwargs={'worker_id': self.pk})

    def get_del_group_url(self):
        return reverse('del_group_from_worker', kwargs={'worker_id': self.pk})




