from django.conf import settings
from django.db import models
from authentication_app.models import CustomUser




class FileUpload(models.Model):
    image = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name


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

    def update_min_values(self):
        min_price = self.details.aggregate(models.Min('price'))['price__min']
        self.min_price = min_price if min_price is not None else 0.00
        min_delivery_time = self.details.aggregate(models.Min('delivery_time_in_days'))['delivery_time_in_days__min']
        self.min_delivery_time = min_delivery_time if min_delivery_time is not None else 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_min_values()
        super().save(update_fields=['min_price', 'min_delivery_time'])


    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=255, default="Default Detail Title")
    revisions = models.IntegerField(help_text="Anzahl der Überarbeitungen (-1 für unendlich)", null=True, blank=True)
    delivery_time_in_days = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    features = models.JSONField(null=True, blank=True)
    offer_type = models.CharField(max_length=20, choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')], null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.offer_type})"


class Order(models.Model):
    customer_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_orders')
    business_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='business_orders')
    title = models.CharField(max_length=255, default="Default Order Title")
    revisions = models.IntegerField(help_text="Anzahl der Überarbeitungen (-1 für unendlich)", null=True, blank=True)
    delivery_time_in_days = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    features = models.JSONField(null=True, blank=True)
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

    def __str__(self):
        return f"BaseInfo: {self.review_count}, Rating: {self.average_rating}, Offers: {self.offer_count}"



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
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=20, choices=[('business', 'Business'), ('customer', 'Customer')], default='customer')


    def __str__(self):
        return f"{self.username} ({self.type})"



class Review(models.Model):
    business_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_reviews')
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_reviews', blank=True, null=True)
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.business_user.username}"
    

