# Generated by Django 4.1.3 on 2022-12-23 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('offer', '0011_remove_room_main_room_remove_room_offer_ptr_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('offer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='offer.offer')),
                ('rooms', models.SmallIntegerField(verbose_name='комнат')),
                ('floors', models.SmallIntegerField(verbose_name='этажей')),
                ('beds', models.SmallIntegerField(verbose_name='спальных мест')),
                ('square', models.FloatField(verbose_name='площадь')),
                ('main_room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='child_rooms', related_query_name='child_room', to='room.room', verbose_name='номер представитель')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('offer.offer',),
        ),
    ]
