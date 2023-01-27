from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse

from ..user.models import CustomUser
# Create your models here.


class Client(CustomUser):
    # TODO: сделать прокси?
    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = False

        super().save(*args, **kwargs)

    def get_admin_show_url(self):
        return reverse('admin_show_client', kwargs={'client_id': self.pk})

    def get_admin_edit_url(self):
        return reverse('admin_edit_client', kwargs={'client_id': self.pk})

    def get_admin_delete_url(self):
        return reverse('admin_delete_client', kwargs={'client_id': self.pk})


# @receiver(pre_save, sender=Client)
# def update_user(sender, instance, **kwargs):
#     print('ssssss!!')
#     instance.user.save()


