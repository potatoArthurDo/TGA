# Generated by Django 5.1.2 on 2024-10-23 18:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0003_collection_is_active'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('shipping_address', models.TextField(max_length=15000)),
                ('amount_paid', models.DecimalField(decimal_places=0, max_digits=15)),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('date_delivered', models.DateTimeField(blank=True, null=True)),
                ('shipped', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=0, max_digits=15)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAdress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_full_name', models.CharField(max_length=200)),
                ('shipping_email', models.CharField(max_length=200)),
                ('shipping_address1', models.CharField(max_length=200)),
                ('shipping_address2', models.CharField(max_length=200)),
                ('shipping_city', models.CharField(max_length=200)),
                ('shipping_country', models.CharField(max_length=200)),
                ('shipping_district', models.CharField(max_length=200)),
                ('shipping_ward', models.CharField(max_length=200)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Shipping Adresses',
            },
        ),
    ]