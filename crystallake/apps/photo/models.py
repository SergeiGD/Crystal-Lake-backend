import base64

from django.db import models

from ..offer.models import Offer
from ..core.build_photo_path import build_photo_path


# Create your models here.


class Photo(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='photos', related_query_name='photo')
    order = models.SmallIntegerField()
    path = models.ImageField(upload_to=build_photo_path)

    class Meta:
        ordering = ['order']

    def get_base64(self):
        base64_str = base64.b64encode(self.path.read()).decode('utf-8')
        ext = self.path.url.split('.')[-1]
        return f'data:image/{ext};base64,{base64_str}'
