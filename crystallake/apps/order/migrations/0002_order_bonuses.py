# Generated by Django 4.1.3 on 2023-01-04 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='bonuses',
            field=models.IntegerField(default=0, verbose_name='Бонусов списано'),
        ),
    ]
