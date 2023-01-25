# Generated by Django 4.1.3 on 2023-01-07 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0002_alter_worker_additional_info'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceTimetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='Начало')),
                ('end', models.DateTimeField(verbose_name='Конце')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetables', related_query_name='timetable', to='service.service', verbose_name='услуга')),
                ('workers', models.ManyToManyField(related_name='timetables', related_query_name='timetable', to='worker.worker', verbose_name='Сотрудники')),
            ],
        ),
        migrations.AddIndex(
            model_name='servicetimetable',
            index=models.Index(fields=['start', 'end'], name='service_ser_start_1b5bd0_idx'),
        ),
    ]