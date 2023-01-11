from decimal import Decimal
from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from polymorphic.models import PolymorphicModel
from django.urls import reverse
from django.utils import timezone

from ..offer.models import Offer
from ..client.models import Client
from .status_choises import get_status_by_code

# Create your models here.


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Клиент')
    comment = models.TextField(verbose_name="комментарий к заказу", blank=True, null=True)
    bonuses = models.IntegerField(verbose_name='Бонусов списано', default=0)
    paid = models.DecimalField(max_digits=12, decimal_places=5, default=0)     # сколько заплатили
    date_create = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    date_full_prepayment = models.DateTimeField(verbose_name="дата полной предоплаты", blank=True, null=True)
    date_full_paid = models.DateTimeField(verbose_name="дата полной оплаты", blank=True, null=True)
    date_finished = models.DateTimeField(verbose_name="дата завершения", blank=True, null=True)
    date_canceled = models.DateTimeField(verbose_name="дата отмены", blank=True, null=True)

    # def check_payment(self):
    #     if self.paid != self.prepayment:
    #         self.date_full_prepayment = None
    #     elif self.date_full_prepayment is None:
    #         self.date_full_prepayment = timezone.now()
    #
    #     if self.paid != self.price:
    #         self.date_full_paid = None
    #     elif self.date_full_paid is None:
    #         self.date_full_paid = timezone.now()
    #
    #     self.save()

    def update_paid(self):
        paid = 0
        for purchase in self.purchases.all():
            if purchase.is_paid and not purchase.is_refund_made:
                paid += purchase.price
            elif purchase.is_paid and purchase.is_refund_made:
                paid += purchase.price - purchase.refund
            elif purchase.is_prepayment_paid:
                paid += purchase.prepayment

        self.paid = paid

        # if self.paid != self.prepayment:
        #     self.date_full_prepayment = None
        # elif self.date_full_prepayment is None:
        #     self.date_full_prepayment = timezone.now()
        if self.paid >= self.prepayment and self.date_full_prepayment is None:
            self.date_full_prepayment = timezone.now()

        if self.paid < self.price:
            self.date_full_paid = None
        elif self.date_full_paid is None:
            self.date_full_paid = timezone.now()

        self.save()

    def mark_as_prepayment_paid(self):
        if not self.date_full_prepayment:
            for purchase in self.purchases.filter(is_canceled=False):
                purchase.is_prepayment_paid = True
                purchase.save()
            self.update_paid()

    def mark_as_paid(self):
        if not self.date_full_paid:
            self.mark_as_prepayment_paid()
            for purchase in self.purchases.filter(is_canceled=False):
                purchase.is_paid = True
                purchase.save()
            self.update_paid()

    # def mark_as_prepayment_unpaid(self):
    #     if self.prepayment > 0:
    #         for purchase in self.purchases.filter(is_canceled=False):
    #             purchase.is_prepayment_paid = False
    #             purchase.is_paid = False
    #             purchase.save()
    #         self.date_full_prepayment = None
    #         self.date_full_paid = None
    #         self.save()

    def mark_as_refund_made(self):
        for purchase in self.purchases.filter(is_canceled=True, is_refund_made=False):
            purchase.is_refund_made = True
            purchase.save()
        self.update_paid()

    def mark_as_canceled(self):
        self.date_canceled = timezone.now()
        self.date_finished = None
        self.save()

    def mark_as_finished(self):
        self.date_canceled = None
        self.date_finished = timezone.now()
        self.save()

    def mark_as_in_process(self):
        self.date_canceled = None
        self.date_finished = None
        self.save()

    @property
    def price(self):
        price = 0
        for purchase in self.purchases.filter(is_canceled=False):
            price += purchase.price
        for purchase in self.purchases.filter(is_canceled=True):
            if purchase.is_paid:
                price += purchase.price - purchase.refund
            else:
                price += purchase.prepayment
        return price

    @property
    def prepayment(self):
        prepayment = 0
        for purchase in self.purchases.filter(is_canceled=False):
            prepayment += purchase.prepayment
        return prepayment

    # @property
    # def paid(self):
    #     paid = 0
    #     for purchase in self.purchases.all():
    #         if purchase.is_full_paid:
    #             paid += purchase.price
    #         else:
    #             paid += purchase.prepayment
    #     return paid

    @property
    def left_to_refund(self):
        left_to_refund = self.paid - self.price
        if left_to_refund > 0:
            return left_to_refund
        return 0

    @property
    def left_to_pay(self):
        left_to_pay = self.price - self.paid
        if left_to_pay > 0:
            return left_to_pay
        return 0

    @property
    def status(self):
        if self.date_finished is not None:
            return get_status_by_code('finished')
        if self.date_canceled is not None:
            return get_status_by_code('canceled')
        return get_status_by_code('in process')

    @property
    def payment_status(self):
        if self.date_full_prepayment is not None:
            return 'Внесена предоплата'
        if self.date_full_paid is not None:
            return 'Полностью оплачен'
        return 'Ожидает предоплату'

    def get_admin_edit_url(self):
        return reverse('admin_edit_order', kwargs={'order_id': self.pk})

    def get_manage_room_purchase_url(self):
        return reverse('manage_room_purchase', kwargs={'order_id': self.pk})

    def get_manage_service_purchase_url(self):
        return reverse('manage_service_purchase', kwargs={'order_id': self.pk})


class Purchase(PolymorphicModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="purchases")
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT, related_name="purchases")

    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    is_prepayment_paid = models.BooleanField(default=False, verbose_name='Предоплата внесена')
    is_refund_made = models.BooleanField(default=False, verbose_name='Средства возвращены')
    is_canceled = models.BooleanField(default=False, verbose_name='Отменено')

    start = models.DateTimeField()
    end = models.DateTimeField()

    price = models.DecimalField(max_digits=12, decimal_places=5)            # итоговая цена
    prepayment = models.DecimalField(max_digits=12, decimal_places=5)       # итоговая предоплата
    refund = models.DecimalField(max_digits=12, decimal_places=5)           # итоговый возврат средств

    def calc_price(self):
        delta_seconds = (self.end - self.start).total_seconds()
        seconds_in_hour = 3600
        seconds_in_day = seconds_in_hour * 24
        if self.offer.price_type == 'hours':
            hours = Decimal(delta_seconds / seconds_in_hour)
            return self.offer.default_price * hours
        if self.offer.price_type == 'days':
            days = Decimal(delta_seconds / seconds_in_day)
            return self.offer.default_price * days
        if self.offer.price_type == 'unit':
            return self.offer.default_price

        raise ValueError('Неизвестный тип цены')

    def calc_prepayment(self):
        prepayment_ratio = Decimal(self.offer.prepayment_percent) / 100
        return self.price * prepayment_ratio

    def calc_refund(self):
        refund_ratio = Decimal(self.offer.refund_percent) / 100
        return self.price * refund_ratio

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__old_is_paid = self.is_paid                    # сохраняем изначальное имя, на случай, если его изменяет
        self.__old_is_prepayment_paid = self.is_prepayment_paid
        self.__old_is_refund_paid = self.is_refund_made
        self.__last_paid = self.get_paid()

    def get_paid(self):
        if self.is_paid and not self.is_refund_made:
            return self.is_paid
        if self.is_paid and self.is_refund_made:
            return self.price - self.refund
        if self.is_prepayment_paid:
            return self.prepayment
        return 0
    def save(self, *args, **kwargs):
        self.price = self.calc_price()
        self.prepayment = self.calc_prepayment()
        self.refund = self.calc_refund()

        # price = self.calc_price()
        # if price != self.__old_price:
        #     self.price = price
        #     self.prepayment = self.calc_prepayemnt()
        #     self.refund = self.calc_refund()
        #     self.order.check_payment()
        # if self.is_paid != self.__old_is_paid or self.is_prepayment_paid != self.__old_is_prepayment_paid:
        #     self.order.calc_paid()

        super().save(*args, **kwargs)

        # self.order.paid -= self.__last_paid
        # self.order.paid += self.get_paid()
        # self.order.save()

        #self.order.update_paid()




    def get_info(self):
        return {
            'name': self.offer.name,
            'link': self.offer.get_admin_show_url(),
            'start': self.start.timestamp(),
            'end': self.end.timestamp(),
            'is_paid': self.is_paid,
            'is_prepayment_paid': self.is_prepayment_paid,
            'id': self.pk
        }

    def get_required_modal(self):
        return 'base modal'

    def cancel(self):
        if self.is_paid or self.is_prepayment_paid:
            self.is_canceled = True
            self.save()
        else:
            self.delete()

    def get_info_url(self):
        return reverse('get_purchase', kwargs={'order_id': self.order.pk, 'purchase_id': self.pk})

    def get_cancel_url(self):
        return reverse('cancel_purchase', kwargs={'order_id': self.order.pk, 'purchase_id': self.pk})


class PurchaseCountable(Purchase):
    quantity = models.SmallIntegerField(default=1)

    def calc_price(self):
        delta_seconds = (self.end - self.start).total_seconds()
        seconds_in_hour = 3600
        seconds_in_day = seconds_in_hour * 24
        if self.offer.price_type == 'hours':
            hours = Decimal(delta_seconds / seconds_in_hour)
            return (self.offer.default_price * hours) * self.quantity
        if self.offer.price_type == 'days':
            days = Decimal(delta_seconds / seconds_in_day)
            return (self.offer.default_price * days) * self.quantity
        if self.offer.price_type == 'unit':
            return self.offer.default_price * self.quantity

        raise ValueError('Неизвестный тип цены')

    def get_info(self):
        data = super().get_info()
        data['quantity'] = self.quantity
        return data

    def get_required_modal(self):
        return 'quantity modal'





