# Generated by Django 4.1.3 on 2022-12-15 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_customuser_phone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['phone']},
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
    ]