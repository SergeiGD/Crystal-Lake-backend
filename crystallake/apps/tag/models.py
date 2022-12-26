from django.db import models
from django.shortcuts import reverse


# Create your models here.


class TagQuerySet(models.QuerySet):
    def search(self, **kwargs):
        qs = self
        if kwargs.get('name', ''):
            qs = qs.filter(name__icontains=kwargs['name'])
        if kwargs.get('id', ''):
            qs = qs.filter(pk=kwargs['id'])
        if kwargs.get('sort_by', ''):
            qs = qs.order_by(kwargs['sort_by'])

        return qs


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)

    objects = TagQuerySet.as_manager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_admin_show_url(self):
        return reverse('admin_show_tag', kwargs={'tag_id': self.pk})

    def get_admin_edit_url(self):
        return reverse('admin_edit_tag', kwargs={'tag_id': self.pk})

    def get_admin_delete_url(self):
        return reverse('admin_delete_tag', kwargs={'tag_id': self.pk})


