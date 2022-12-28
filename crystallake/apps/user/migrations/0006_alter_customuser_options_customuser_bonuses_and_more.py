# Generated by Django 4.1.3 on 2022-12-28 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_customuser_options_remove_customuser_username'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['first_name']},
        ),
        migrations.AddField(
            model_name='customuser',
            name='bonuses',
            field=models.IntegerField(blank=True, default=0, verbose_name='Бонусов'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('male', 'мужской'), ('female', 'женский'), ('unknown', 'не выбрано')], default='unknown', max_length=50, verbose_name='Пол'),
        ),
    ]
