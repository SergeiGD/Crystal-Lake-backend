from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from polymorphic.models import PolymorphicModel

# Create your models here.


class Order(models.Model):
    comment = models.TextField(verbose_name="комментарий к заказу", blank=True, null=True)
    date_create = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    date_full_prepayment = models.DateTimeField(verbose_name="дата полной предоплаты", blank=True, null=True)
    date_full_paid = models.DateTimeField(verbose_name="дата полной оплаты", blank=True, null=True)
    date_full_refund = models.DateTimeField(verbose_name="дата полного возврата", blank=True, null=True)
    date_finished = models.DateTimeField(verbose_name="дата завершения", blank=True, null=True)
    date_canceled = models.DateTimeField(verbose_name="дата отмены", blank=True, null=True)
    is_timeout = models.BooleanField(default=False)


class Purchase(PolymorphicModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="purchases")

    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.BigIntegerField()
    offer = GenericForeignKey("content_type", "object_id")

    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=5)
    unit_prepayment = models.DecimalField(max_digits=12, decimal_places=5)
    unit_refund = models.DecimalField(max_digits=12, decimal_places=5)
    bonus_write_off = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    @property
    def calculated_price(self):
        delta = self.date_end - self.date_start
        return self.unit_price * delta.days


class PurchaseCountable(Purchase):
    quantity = models.SmallIntegerField(default=1)

    @property
    def calculated_price(self):
        return self.quantity * self.unit_price

