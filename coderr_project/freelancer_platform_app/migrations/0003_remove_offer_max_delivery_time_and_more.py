# Generated by Django 5.1.4 on 2024-12-29 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer_platform_app', '0002_offer_max_delivery_time_offer_max_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='max_delivery_time',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='max_price',
        ),
    ]
