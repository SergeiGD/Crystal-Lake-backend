from django.db import models
from django.contrib.auth.models import Group, Permission
from django.urls import reverse

# Create your models here.


class GroupQuerySet(models.QuerySet):
    def search(self, **kwargs):
        qs = self
        if kwargs.get('name', ''):
            qs = qs.filter(name__icontains=kwargs['name'])
        if kwargs.get('id', ''):
            qs = qs.filter(pk=kwargs['id'])
        if kwargs.get('sort_by', ''):
            qs = qs.order_by(kwargs['sort_by'])

        return qs


class PermissionsQuerySet(models.QuerySet):
    def search(self, **kwargs):
        qs = self
        if kwargs.get('name', ''):
            qs = qs.filter(name__icontains=kwargs['name'])
        if kwargs.get('id', ''):
            qs = qs.filter(pk=kwargs['id'])
        if kwargs.get('sort_by', ''):
            qs = qs.order_by(kwargs['sort_by'])

        return qs


class GroupProxy(Group):
    class Meta:
        proxy = True
        ordering = ['-id']

    objects = GroupQuerySet.as_manager()

    def get_admin_show_url(self):
        return reverse('admin_show_group', kwargs={'group_id': self.pk})

    def get_admin_edit_url(self):
        return reverse('admin_edit_group', kwargs={'group_id': self.pk})

    def get_admin_delete_url(self):
        return reverse('admin_delete_group', kwargs={'group_id': self.pk})

    def get_del_permission_url(self):
        return reverse('del_permission_from_group', kwargs={'group_id': self.pk})

    def get_add_permission_url(self):
        return reverse('add_permission_to_group', kwargs={'group_id': self.pk})

    def get_unattached_permissions_url(self):
        return reverse('get_unattached_permissions', kwargs={'group_id': self.pk})


class PermissionsProxy(Permission):         # TODO: удалить дубликаты и подумать, что делать с разрешенияеми на прокси-моделями
    class Meta:
        proxy = True
        ordering = ['-id']

    objects = PermissionsQuerySet.as_manager()

