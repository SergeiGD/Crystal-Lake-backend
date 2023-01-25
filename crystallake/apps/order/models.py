from decimal import Decimal
from datetime import datetime

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from django.contrib.contenttypes.models import ContentType
from polymorphic.models import PolymorphicModel, PolymorphicManager
from django.urls import reverse
from django.utils import timezone

from ..offer.models import Offer
from ..client.models import Client
from .status_choises import get_status_by_code, get_status_by_name, Status

# Create your models here.


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Клиент')
    comment = models.TextField(verbose_name="комментарий к заказу", blank=True, null=True)
    paid = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Оплачено')     # сколько заплатили
    refunded = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Возвращено')
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

    # def update_paid(self):
    #     paid = 0
    #     for purchase in self.purchases.all():
    #         if purchase.is_paid and not purchase.is_refund_made:
    #             paid += purchase.price
    #         elif purchase.is_paid and purchase.is_refund_made:
    #             paid += purchase.price - purchase.refund
    #         elif purchase.is_prepayment_paid:
    #             paid += purchase.prepayment
    #
    #     self.paid = paid
    #     if self.paid >= self.prepayment and self.date_full_prepayment is None:
    #         self.date_full_prepayment = timezone.now()
    #
    #     if self.paid < self.price:
    #         self.date_full_paid = None
    #     elif self.date_full_paid is None:
    #         self.date_full_paid = timezone.now()
    #
    #     self.save()

        # if self.paid != self.prepayment:
        #     self.date_full_prepayment = None
        # elif self.date_full_prepayment is None:
        #     self.date_full_prepayment = timezone.now()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.pk:
            self.__original_paid,  self.__original_price = self.paid,  self.price
        self.__original_paid, self.__original_price = 0, 0

    def save(self, *args, **kwargs):
        if self.pk and (self.__original_paid != self.paid or self.__original_price != self.price):
            self.check_payment()
        super().save(*args, **kwargs)

    def check_payment(self):
        if self.paid >= self.prepayment:
            self.purchases.filter(is_canceled=False).update(is_prepayment_paid=True)
            if self.date_full_prepayment is None:
                self.date_full_prepayment = timezone.now()

        print(self.paid)
        print(self.price)
        if self.paid >= self.price:
            print(11111)
            self.purchases.filter(is_canceled=False).update(is_paid=True)
            if self.date_full_paid is None:
                self.date_full_paid = timezone.now()

        if self.paid < self.prepayment and self.date_full_prepayment is not None:
            self.date_full_prepayment = None
            if self.paid < self.__original_paid:
                self.purchases.filter(is_canceled=False).update(is_prepayment_paid=False)

        if self.paid < self.price and self.date_full_paid is not None:
            self.date_full_paid = None
            if self.paid < self.__original_paid:
                self.purchases.filter(is_canceled=False).update(is_paid=False)


    # def mark_as_prepayment_paid(self):
    #     if not self.date_full_prepayment and self.price > 0:
    #         for purchase in self.purchases.filter(is_canceled=False):
    #             purchase.is_prepayment_paid = True
    #             purchase.save()
    #         self.update_paid()
    #
    # def mark_as_paid(self):
    #     if not self.date_full_paid and self.price > 0:
    #         self.mark_as_prepayment_paid()
    #         for purchase in self.purchases.filter(is_canceled=False):
    #             purchase.is_paid = True
    #             purchase.save()
    #         self.update_paid()

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
        refund_made = self.left_to_refund
        self.paid -= refund_made
        self.refunded += refund_made
        self.save()

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

    def is_editable(self):
        if self.status == Status.finished.value or self.status == Status.canceled.value:
            return False
        return True

    @property
    def price(self):
        price = 0
        for purchase in self.purchases.all():
            if purchase.is_canceled and purchase.is_paid:
                price += purchase.price - purchase.refund
            elif purchase.is_canceled and not purchase.is_paid:
                price += purchase.prepayment
            elif not purchase.is_canceled:
                price += purchase.price

        return price

        # for purchase in self.purchases.filter(is_canceled=False):
        #     price += purchase.price
        # for purchase in self.purchases.filter(is_canceled=True):
        #     if purchase.is_paid:
        #         price += purchase.price - purchase.refund
        #     else:
        #         price += purchase.prepayment
        # return price

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
            return Status.finished.value
        if self.date_canceled is not None:
            return Status.canceled.value
        return Status.process.value

    @property
    def payment_status(self):
        if self.date_full_paid is not None:
            return 'Полностью оплачен'
        if self.date_full_prepayment is not None:
            return 'Внесена предоплата'
        return 'Ожидает предоплату'

    def get_admin_edit_url(self):
        return reverse('admin_edit_order', kwargs={'order_id': self.pk})

    def get_admin_show_url(self):
        return reverse('admin_show_order', kwargs={'order_id': self.pk})

    def get_create_room_purchase_url(self):
        return reverse('create_room_purchase', kwargs={'order_id': self.pk})

    def get_create_service_purchase_url(self):
        return reverse('create_service_purchase', kwargs={'order_id': self.pk})

    class Meta:
        ordering = ['-date_create']


class PurchaseManager(PolymorphicManager):
    def update_order_decorator(bulk_func):
        """
        ДЕКОРАТОР ДЛЯ ОБНОВЛЕНИЯ ЗАКАЗА ПОСЛЕ ДОБАВЛЕНИЯ ЭЛЕМЕНТОВ
        """
        from functools import wraps
        @wraps(bulk_func)
        def wrapper(*args, **kwargs):
            purchases = bulk_func(*args, **kwargs)
            if len(purchases) > 0:
                order = purchases[0].order
                order.save()

        return wrapper

    @update_order_decorator
    def bulk_create(self, purchases, **kwargs):
        for purchase in purchases:
            purchase.clean()
            purchase.price = purchase.calc_price()
            purchase.prepayment = purchase.calc_prepayment()
            purchase.refund = purchase.calc_refund()
            if not purchase.is_canceled:
                purchase.is_paid = False
                purchase.is_prepayment_paid = False
        return super(PurchaseManager, self).bulk_create(purchases, **kwargs)


class Purchase(PolymorphicModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="purchases")
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT, related_name="purchases")

    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    is_prepayment_paid = models.BooleanField(default=False, verbose_name='Предоплата внесена')
    is_refund_made = models.BooleanField(default=False, verbose_name='Средства возвращены')
    is_canceled = models.BooleanField(default=False, verbose_name='Отменено')

    start = models.DateTimeField()
    end = models.DateTimeField()

    price = models.DecimalField(max_digits=12, decimal_places=2)            # итоговая цена
    prepayment = models.DecimalField(max_digits=12, decimal_places=2)       # итоговая предоплата
    refund = models.DecimalField(max_digits=12, decimal_places=2)           # итоговый возврат средств

    objects = PurchaseManager()

    def get_payment_status(self):
        if self.is_paid:
            return 'Оплачен'
        if self.is_prepayment_paid:
            return 'Предоплата'
        return 'Нет'

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

        raise ValueError('Неизвестный тип цены')

    def calc_prepayment(self):
        prepayment_ratio = Decimal(self.offer.prepayment_percent) / 100
        return self.price * prepayment_ratio

    def calc_refund(self):
        refund_ratio = Decimal(self.offer.refund_percent) / 100
        return self.price * refund_ratio

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.__old_is_paid = self.is_paid                    # сохраняем изначальное имя, на случай, если его изменяет
    #     self.__old_is_prepayment_paid = self.is_prepayment_paid
    #     self.__old_is_refund_paid = self.is_refund_made
    #     self.__last_paid = self.get_paid()

    def get_paid(self):
        if self.is_paid and not self.is_refund_made:
            return self.is_paid
        if self.is_paid and self.is_refund_made:
            return self.price - self.refund
        if self.is_prepayment_paid:
            return self.prepayment
        return 0

    def save(self, *args, **kwargs):
        # self.clean()
        self.price = self.calc_price()
        self.prepayment = self.calc_prepayment()
        self.refund = self.calc_refund()
        if not self.is_canceled:
            self.is_paid = False
            self.is_prepayment_paid = False
        super().save(*args, **kwargs)
        order = self.order
        order.save()

        # self.order.update_payment_status()

    # def clean(self):
    #     from django.core.exceptions import ValidationError
    #
    #     if not self.pk and self.order.date_full_prepayment:
    #         raise ValidationError('Нельзя добавить покупки к уже подтвержденному заказу')
    #
    #     if self.order.date_canceled or self.order.date_finished:
    #         raise ValidationError('Нельзя изменить завершенный заказ')
    #
    #     if self.pk and self.order.date_full_paid:
    #         raise ValidationError('Нельзя изменить покупки оплаченного заказа заказ заказу')

    def get_info(self):

        return {
            'offer': self.offer.get_info(),
            'start': self.start.timestamp(),
            'end': self.end.timestamp(),
            'is_paid': self.is_paid,
            'is_prepayment_paid': self.is_prepayment_paid,
            'id': self.pk,
            'edit_url': self.get_edit_url()
        }

    def cancel(self):
        if self.is_paid or self.is_prepayment_paid:
            self.is_canceled = True
            self.save()
        else:
            order = self.order
            self.delete()
            order.save()


    def get_info_url(self):
        return reverse('get_purchase', kwargs={'order_id': self.order.pk, 'purchase_id': self.pk})

    def get_cancel_url(self):
        return reverse('cancel_purchase', kwargs={'order_id': self.order.pk, 'purchase_id': self.pk})

    def get_edit_url(self):
        return reverse('edit_room_purchase', kwargs={'order_id': self.order.pk, 'purchase_id': self.pk})


class PurchaseCountable(Purchase):
    quantity = models.SmallIntegerField(default=1)

    # def clean(self):
    #     from django.core.exceptions import ValidationError
    #
    #     if self.quantity > self.offer.max_in_group:
    #         raise ValidationError('Превышено максимальное количество')

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

        raise ValueError('Неизвестный тип цены')

    def get_info(self):
        data = super().get_info()
        data['quantity'] = self.quantity
        return data

    def get_edit_url(self):
        return reverse('edit_service_purchase', kwargs={'order_id': self.order.pk, 'purchase_id': self.pk})


# @receiver(pre_save, sender=Purchase)
# def purchase_save_handler(sender, instance, *args, **kwargs):
#     print('asdsadsadsadsd')
#     instance.clean()
#     instance.price = instance.calc_price()
#     instance.prepayment = instance.calc_prepayment()
#     instance.refund = instance.calc_refund()


# @receiver(pre_save, sender=Purchase)
# def update_user(sender, instance, **kwargs):
#     print('ssssss!!')
#     instance.user.save()



