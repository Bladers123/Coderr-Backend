from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from authentication_app.models import CustomUser
from ..models import OfferDetail, Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, username=instance.username, first_name=instance.first_name, last_name=instance.last_name, email=instance.email)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=OfferDetail)
@receiver(post_delete, sender=OfferDetail)
def update_offer_min_values(sender, instance, **kwargs):
    if instance.offer:
        offer = instance.offer
        offer.update_min_values()
        offer.save()


@receiver(post_save, sender=CustomUser)
def sync_profile_type(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.type = instance.type
        instance.profile.save()