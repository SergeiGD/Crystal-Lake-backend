# Generated by Django 4.1.3 on 2022-12-23 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0002_alter_tag_options'),
        ('offer', '0010_auto_20221223_0949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='main_room',
        ),
        migrations.RemoveField(
            model_name='room',
            name='offer_ptr',
        ),
        migrations.RemoveField(
            model_name='service',
            name='offer_ptr',
        ),
        migrations.AlterField(
            model_name='offer',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='offers', related_query_name='offer', to='tag.tag'),
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
        migrations.DeleteModel(
            name='Service',
        ),
    ]
