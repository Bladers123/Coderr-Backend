from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from authentication_app.models import CustomUser



# User = get_user_model()


class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)



class Offer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='offers', default=1)
    title = models.CharField(max_length=255, default="Default Title")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator_id = models.IntegerField(CustomUser, default=1)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    min_delivery_time = models.IntegerField(help_text="Minimum delivery time in days", default=1)
    image = models.ForeignKey(FileUpload, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=255, default="Default Detail Title")
    revisions = models.IntegerField(help_text="Anzahl der Überarbeitungen (-1 für unendlich)", null=True, blank=True)
    delivery_time_in_days = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    features = models.JSONField(null=True, blank=True)  # Liste von Features
    offer_type = models.CharField(max_length=20, choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')], null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.offer_type})"


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders', default=1)
    customer_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_orders')
    business_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='business_orders')
    title = models.CharField(max_length=255, default="Default Order Title")
    revisions = models.IntegerField(help_text="Anzahl der Überarbeitungen (-1 für unendlich)", null=True, blank=True)
    delivery_time_in_days = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    features = models.JSONField(null=True, blank=True)  # Liste von Features
    offer_type = models.CharField(max_length=20, choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')], null=True, blank=True)
    status = models.CharField(max_length=20, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} for {self.offer.title} - {self.offer_detail.title}"
    




class BaseInfo(models.Model):
    review_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    business_profile_count = models.IntegerField(default=0)
    offer_count = models.IntegerField(default=0)




class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    file = models.ForeignKey('FileUpload', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=20, choices=[('business', 'Business'), ('customer', 'Customer')], default='customer')
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.type})"

class BusinessProfile(Profile):
    business_name = models.CharField(max_length=255)

    def __str__(self):
        return self.business_name

class CustomerProfile(Profile):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=255)

    def __str__(self):
        return self.customer_name




class Review(models.Model):
    business_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_reviews')
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_reviews')
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    