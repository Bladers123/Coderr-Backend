# Generated by Django 5.1.4 on 2025-01-02 15:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer_platform_app', '0020_completedordercount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_count', models.IntegerField(default=0)),
                ('average_rating', models.FloatField(default=0.0)),
                ('business_profile_count', models.IntegerField(default=0)),
                ('offer_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('tel', models.CharField(blank=True, max_length=20)),
                ('description', models.TextField(blank=True)),
                ('working_hours', models.CharField(blank=True, max_length=255)),
                ('type', models.CharField(blank=True, choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')], max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='freelancer_platform_app.fileupload')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessProfile',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='freelancer_platform_app.profile')),
                ('business_name', models.CharField(max_length=255)),
            ],
            bases=('freelancer_platform_app.profile',),
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='freelancer_platform_app.profile')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('customer_name', models.CharField(max_length=255)),
            ],
            bases=('freelancer_platform_app.profile',),
        ),
    ]