# Generated by Django 4.1.3 on 2023-01-30 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_smscode_request_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smscode',
            name='request_code',
        ),
    ]
