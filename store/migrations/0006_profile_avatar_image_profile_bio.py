# Generated by Django 4.2.9 on 2024-11-15 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_product_colors_product_sizes_productinventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar_image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/avatars/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]