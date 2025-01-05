# Generated by Django 5.1.4 on 2025-01-04 22:51

import authentication_app.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('type', models.CharField(choices=[('business', 'Business'), ('customer', 'Customer')], default='customer', max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
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
        migrations.AddField(
            model_name='profile',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='freelancer_platform_app.fileupload'),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Default Title', max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('creator_id', models.IntegerField(default=1, verbose_name=authentication_app.models.CustomUser)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('min_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('min_delivery_time', models.IntegerField(default=1, help_text='Minimum delivery time in days')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='freelancer_platform_app.fileupload')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='offers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OfferDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Default Detail Title', max_length=255)),
                ('revisions', models.IntegerField(blank=True, help_text='Anzahl der Überarbeitungen (-1 für unendlich)', null=True)),
                ('delivery_time_in_days', models.PositiveIntegerField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('features', models.JSONField(blank=True, null=True)),
                ('offer_type', models.CharField(blank=True, choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')], max_length=20, null=True)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='freelancer_platform_app.offer')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Default Order Title', max_length=255)),
                ('revisions', models.IntegerField(blank=True, help_text='Anzahl der Überarbeitungen (-1 für unendlich)', null=True)),
                ('delivery_time_in_days', models.PositiveIntegerField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('features', models.JSONField(blank=True, null=True)),
                ('offer_type', models.CharField(blank=True, choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')], max_length=20, null=True)),
                ('status', models.CharField(default='in_progress', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_orders', to=settings.AUTH_USER_MODEL)),
                ('customer_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_orders', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_reviews', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='given_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
