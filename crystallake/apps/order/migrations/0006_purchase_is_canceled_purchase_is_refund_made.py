# Generated by Django 4.1.3 on 2023-01-06 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_remove_purchase_bonus_write_off_order_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='is_canceled',
            field=models.BooleanField(default=False, verbose_name='Отменено'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='is_refund_made',
            field=models.BooleanField(default=False, verbose_name='Средства возвращены'),
        ),
    ]
