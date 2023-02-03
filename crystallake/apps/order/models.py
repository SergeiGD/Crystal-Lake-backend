from decimal import Decimal

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from django.contrib.contenttypes.models import ContentType
from polymorphic.models import PolymorphicModel, PolymorphicManager
from django.urls import reverse
from django.utils import timezone
from django.db.models import Max

from ..offer.models import Offer
# from ..client.models import Client
from .status_choises import get_status_by_code, get_status_by_name, Status
from ..offer.price_choises import PriceType

# Create your models here.


class Order(models.Model):
    # client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Клиент')
    client = models.ForeignKey("user.CustomUser", on_delete=models.PROTECT, verbose_name='Клиент')
    comment = models.TextField(verbose_name="комментарий к заказу", blank=True, null=True)
    paid = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Оплачено')     # сколько заплатили
    refunded = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Возвращено')
    date_create = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    date_full_prepayment = models.DateTimeField(verbose_name="дата полной предоплаты", blank=True, null=True)
    date_full_paid = models.DateTimeField(verbose_name="дата полной оплаты", blank=True, null=True)
    date_finished = models.DateTimeField(verbose_name="дата завершения", blank=True, null=True)
    date_canceled = models.DateTimeField(verbose_name="дата отмены", blank=True, null=True)

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

        if self.paid >= self.price:
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

    def mark_as_prepayment_paid(self):
        self.paid = self.prepayment
        self.save()

    def mark_as_fully_paid(self):
        self.paid = self.price
        self.save()

    def mark_as_refund_made(self):
        for purchase in self.purchases.filter(is_canceled=True, is_refund_made=False):
            purchase.is_refund_made = True
            purchase.save()
        refund_made = self.left_to_refund
        self.paid -= refund_made
        self.refunded += refund_made
        self.save()

    def mark_as_canceled(self):
        if self.is_cancelable():
            self.date_canceled = timezone.now()
            self.date_finished = None
            for purchase in self.purchases.filter(is_canceled=False):
                purchase.cancel()
            self.save()

    def mark_as_finished(self):
        if self.is_finishable():
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

    def is_cancelable(self):
        if self.date_canceled is not None:
            return False
        # if self.purchases.filter(start__lte=timezone.now(), is_canceled=False).exists():
        #     return False
        return True

    def is_finishable(self):
        if self.date_full_paid is None or self.date_finished is not None:
            return False
        return True

    @property
    def price(self):
        price = 0
        if not self.pk:
            return 0
        for purchase in self.purchases.all():
            if purchase.is_canceled and purchase.is_paid:
                price += purchase.price - purchase.refund
            elif purchase.is_canceled and not purchase.is_paid:
                price += purchase.prepayment
            elif not purchase.is_canceled:
                price += purchase.price

        return price

    @property
    def prepayment(self):
        prepayment = 0
        if not self.pk:
            return 0
        for purchase in self.purchases.filter(is_canceled=False):
            prepayment += purchase.prepayment
        return prepayment

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

    @property
    def main_offer(self):
        if self.get_active_purchases().count() > 0:
            main_purchase = self.purchases.filter(is_canceled=False).order_by('-price').first()
            return main_purchase.offer
        main_purchase = self.purchases.order_by('-price').first()
        if main_purchase is not None:
            return main_purchase.offer

    @property
    def name(self):
        purchases_count = self.purchases.count()
        if purchases_count > 1:
            return f'{self.main_offer.name} и еще {purchases_count - 1} покупок'
        if self.main_offer is not None:
            return self.main_offer.name
        return f'Заказ от {self.date_create.date()}'

    @property
    def is_cart(self):
        if self.paid == 0 and self.refunded == 0 and self.date_canceled is None and self.date_finished is None:
            return True
        return False

    def get_active_purchases(self):
        return self.purchases.filter(is_canceled=False)

    def get_admin_edit_url(self):
        return reverse('admin_edit_order', kwargs={'order_id': self.pk})

    def get_admin_show_url(self):
        return reverse('admin_show_order', kwargs={'order_id': self.pk})

    def get_create_room_purchase_url(self):
        return reverse('create_room_purchase', kwargs={'order_id': self.pk})

    def get_create_service_purchase_url(self):
        return reverse('create_service_purchase', kwargs={'order_id': self.pk})

    def get_client_manage_url(self):
        return reverse('client_manage_order', kwargs={'order_id': self.pk})

    def get_client_cancel_url(self):
        return reverse('client_cancel_order', kwargs={'order_id': self.pk})

    def get_client_pay_url(self):
        return reverse('client_pay', kwargs={'order_id': self.pk})

    def get_client_history_url(self):
        return reverse('history_item', kwargs={'order_id': self.pk})

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

    def get_status(self):
        if self.is_canceled:
            return 'Отменен'
        if self.is_paid:
            return 'Оплачен'
        if self.is_prepayment_paid:
            return 'Предоплата'
        return 'Нет'

    def calc_price(self):
        delta_seconds = (self.end - self.start).total_seconds()
        seconds_in_hour = 3600
        seconds_in_day = seconds_in_hour * 24
        if self.offer.price_type == PriceType.hour.name:
            hours = round(Decimal(delta_seconds / seconds_in_hour), 0)
            return self.offer.default_price * hours
        if self.offer.price_type == PriceType.day.name:
            days = round(Decimal(delta_seconds / seconds_in_day), 0)
            return self.offer.default_price * days

        raise ValueError('Неизвестный тип цены')

    def calc_prepayment(self):
        prepayment_ratio = Decimal(self.offer.prepayment_percent) / 100
        return self.price * prepayment_ratio

    def calc_refund(self):
        refund_ratio = Decimal(self.offer.refund_percent) / 100
        return self.price * refund_ratio

    def save(self, *args, **kwargs):
        self.price = self.calc_price()
        self.prepayment = self.calc_prepayment()
        self.refund = self.calc_refund()
        if not self.is_canceled:
            self.is_paid = False
            self.is_prepayment_paid = False
        super().save(*args, **kwargs)
        order = self.order
        order.save()

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
        if not self.order.purchases.exclude(pk=self.id).filter(is_canceled=False).exists() and self.order.date_canceled is None:
            self.order.mark_as_canceled()
            return
        if self.is_paid or self.is_prepayment_paid:
            self.is_canceled = True
            self.save()
        else:
            order = self.order
            self.delete()
            order.save()

    def is_editable(self):
        if self.is_canceled or self.end <= timezone.now() or not self.order.is_editable():
            return False
        return True

    def get_info_url(self):
        return reverse('get_purchase', kwargs={'order_id': self.order.pk, 'purchase_id': self.pk})

    def get_cancel_url(self):
        return reverse('cancel_purchase', kwargs={'order_id': self.order.pk, 'purchase_id': self.pk})

    def get_remove_cart_item_url(self):
        return reverse('remove_cart_item', kwargs={'purchase_id': self.pk})

    def get_client_edit_url(self):
        return reverse('client_manage_purchase', kwargs={'purchase_id': self.pk, 'order_id': self.order.pk})

    def get_client_save_changes_url(self):
        return reverse('client_save_room_changes', kwargs={'purchase_id': self.pk, 'order_id': self.order.pk})

    def get_client_cancel_url(self):
        return reverse('client_cancel_purchase', kwargs={'order_id': self.order.pk, 'purchase_id': self.pk})

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

    def get_client_save_changes_url(self):
        return reverse('client_save_service_changes', kwargs={'purchase_id': self.pk, 'order_id': self.order.pk})


