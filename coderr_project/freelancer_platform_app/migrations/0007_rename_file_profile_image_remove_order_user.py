# Generated by Django 5.1.4 on 2025-01-25 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer_platform_app', '0006_profile_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='file',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
    ]
