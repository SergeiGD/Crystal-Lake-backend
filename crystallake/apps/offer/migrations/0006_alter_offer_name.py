# Generated by Django 4.1.3 on 2022-12-14 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0005_alter_offer_default_price_alter_offer_weekend_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='наименование'),
        ),
    ]