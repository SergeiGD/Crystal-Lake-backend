# Generated by Django 4.1.3 on 2022-12-26 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0011_remove_room_main_room_remove_room_offer_ptr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='name',
            field=models.CharField(max_length=255, verbose_name='наименование'),
        ),
    ]
