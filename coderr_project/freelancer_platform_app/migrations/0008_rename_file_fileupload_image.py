# Generated by Django 5.1.4 on 2025-01-25 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer_platform_app', '0007_rename_file_profile_image_remove_order_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fileupload',
            old_name='file',
            new_name='image',
        ),
    ]
