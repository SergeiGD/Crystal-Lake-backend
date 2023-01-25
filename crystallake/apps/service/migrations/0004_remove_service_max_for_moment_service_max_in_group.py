# Generated by Django 4.1.3 on 2023-01-19 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_alter_servicetimetable_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='max_for_moment',
        ),
        migrations.AddField(
            model_name='service',
            name='max_in_group',
            field=models.SmallIntegerField(default=1, verbose_name='макс. в группе'),
        ),
    ]