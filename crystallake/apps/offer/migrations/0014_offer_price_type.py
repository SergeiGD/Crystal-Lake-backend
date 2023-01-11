# Generated by Django 4.1.3 on 2023-01-03 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0013_alter_offer_description_alter_offer_main_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='price_type',
            field=models.CharField(choices=[('hours', 'часы'), ('days', 'дни')], default='hours', max_length=50, verbose_name='Цена за'),
        ),
    ]
