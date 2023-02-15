from ..order.models import Order
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


def clean_orders_job():
    Order.objects.filter(
        paid=0,
        refunded=0,
        date_create__lt=make_aware(datetime.now() - timedelta(hours=12))
    ).delete()

