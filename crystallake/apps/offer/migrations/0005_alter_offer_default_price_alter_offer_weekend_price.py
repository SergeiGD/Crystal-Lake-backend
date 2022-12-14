# Generated by Django 4.1.3 on 2022-12-14 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0004_alter_offer_main_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='default_price',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='стандартная цена'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='weekend_price',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='праздничная цена'),
        ),
    ]
