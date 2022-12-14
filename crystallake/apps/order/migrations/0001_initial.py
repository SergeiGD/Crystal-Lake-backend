# Generated by Django 4.1.3 on 2023-01-03 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('offer', '0014_offer_price_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='комментарий к заказу')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('date_full_prepayment', models.DateTimeField(blank=True, null=True, verbose_name='дата полной предоплаты')),
                ('date_full_paid', models.DateTimeField(blank=True, null=True, verbose_name='дата полной оплаты')),
                ('date_full_refund', models.DateTimeField(blank=True, null=True, verbose_name='дата полного возврата')),
                ('date_finished', models.DateTimeField(blank=True, null=True, verbose_name='дата завершения')),
                ('date_canceled', models.DateTimeField(blank=True, null=True, verbose_name='дата отмены')),
                ('is_timeout', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='client.client', verbose_name='Клиент')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_full_paid', models.BooleanField(default=False, verbose_name='Оплачено')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('price', models.DecimalField(decimal_places=5, max_digits=12)),
                ('prepayment', models.DecimalField(decimal_places=5, max_digits=12)),
                ('refund', models.DecimalField(decimal_places=5, max_digits=12)),
                ('bonus_write_off', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchases', to='offer.offer')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchases', to='order.order')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='PurchaseCountable',
            fields=[
                ('purchase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='order.purchase')),
                ('quantity', models.SmallIntegerField(default=1)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('order.purchase',),
        ),
    ]
