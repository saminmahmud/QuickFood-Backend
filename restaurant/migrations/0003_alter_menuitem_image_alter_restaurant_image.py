# Generated by Django 5.1.7 on 2025-03-29 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_remove_menuitem_menu_menuitem_restaurant_delete_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(blank=True, upload_to='menu_item_image/'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(blank=True, upload_to='restaurant_image/'),
        ),
    ]
