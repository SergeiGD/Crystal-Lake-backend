# Generated by Django 4.1.3 on 2023-01-30 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_smscode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smscode',
            name='code',
            field=models.TextField(verbose_name='Код'),
        ),
    ]
