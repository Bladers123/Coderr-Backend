# Generated by Django 5.1.4 on 2024-12-31 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer_platform_app', '0012_offerdetail_offer_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='min_delivery_time',
            field=models.IntegerField(default=1, help_text='Minimum delivery time in days'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='min_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
