from django.db import models
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters



User = get_user_model()


class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)



class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers', default=1)
    title = models.CharField(max_length=255, default="Default Title")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    min_delivery_time = models.IntegerField(help_text="Minimum delivery time in days", blank=True, null=True)
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


