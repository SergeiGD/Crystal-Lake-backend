# Generated by Django 4.1.3 on 2022-12-03 09:03

import apps.offer.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_main', models.BooleanField(default=False)),
                ('order', models.SmallIntegerField()),
                ('path', models.ImageField(upload_to=apps.offer.models.build_photo_path)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='offer.offer')),
            ],
        ),
    ]
