# Generated by Django 4.1.3 on 2023-02-06 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0023_alter_offer_price_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='price_type',
            field=models.CharField(choices=[('hour', 'час'), ('day', 'сутки')], default='day', max_length=50, verbose_name='Цена за'),
        ),
    ]
