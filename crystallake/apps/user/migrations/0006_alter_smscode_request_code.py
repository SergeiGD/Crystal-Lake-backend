# Generated by Django 4.1.3 on 2023-01-30 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_smscode_is_used_smscode_request_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smscode',
            name='request_code',
            field=models.TextField(unique=True, verbose_name='Иднетификатор запроса'),
        ),
    ]
