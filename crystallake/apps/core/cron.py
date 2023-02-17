from ..order.models import Order, Purchase
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


def clean_orders_job():
    Order.objects.filter(
        paid=0,
        refunded=0,
        date_create__lt=make_aware(datetime.now() - timedelta(hours=12))
    ).delete()


def finish_orders_job():
    finished_orders = Order.objects.filter(
        date_finished=None,
        date_canceled=None,
    ).exclude(
        purchases__in=Purchase.objects.filter(
            end__lte=make_aware(datetime.now())
        )
    )

    for order in finished_orders:
        order.mark_as_finished()

