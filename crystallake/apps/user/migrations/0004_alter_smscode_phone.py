# Generated by Django 4.1.3 on 2023-01-30 11:45

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_smscode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smscode',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='RU', verbose_name='Номер телефона'),
        ),
    ]