# Generated by Django 5.1.4 on 2025-01-25 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer_platform_app', '0008_rename_file_fileupload_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='image',
            new_name='file',
        ),
    ]
