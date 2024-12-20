# Generated by Django 5.1.2 on 2024-12-20 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='colors',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='sizes',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
