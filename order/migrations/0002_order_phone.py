# Generated by Django 4.2.7 on 2025-03-19 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default=1, max_length=13),
            preserve_default=False,
        ),
    ]
