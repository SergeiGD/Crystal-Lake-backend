# Generated by Django 4.1.3 on 2023-01-21 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0015_alter_offer_price_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='price_type',
            field=models.CharField(choices=[('hours', 'часы'), ('days', 'дни')], default='days', max_length=50, verbose_name='Цена за'),
        ),
    ]