# Generated by Django 4.1.3 on 2023-01-26 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0018_rename__main_photo_offer_main_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offer',
            old_name='main_photo',
            new_name='_main_photo',
        ),
    ]
