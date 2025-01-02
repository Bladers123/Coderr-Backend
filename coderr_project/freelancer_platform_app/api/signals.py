from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ..models import Order, OrderCount

@receiver(post_save, sender=Order)
@receiver(post_delete, sender=Order)
def update_order_count(sender, instance, **kwargs):
    business_user = instance.business_user
    order_count = Order.objects.filter(business_user=business_user).count()

    # Aktualisiere oder erstelle den OrderCount-Eintrag
    OrderCount.objects.update_or_create(
        business_user=business_user,
        defaults={"order_count": order_count}
    )