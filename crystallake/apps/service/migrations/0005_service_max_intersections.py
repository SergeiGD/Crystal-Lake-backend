# Generated by Django 4.1.3 on 2023-01-21 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_remove_service_max_for_moment_service_max_in_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='max_intersections',
            field=models.SmallIntegerField(default=1, verbose_name='макс пересечений'),
        ),
    ]
