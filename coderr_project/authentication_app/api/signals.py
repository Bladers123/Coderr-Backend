from django.db.models.signals import post_migrate
from django.dispatch import receiver
from ..models import CustomUser



@receiver(post_migrate)
def create_default_users(sender, **kwargs):
    if not CustomUser.objects.filter(username='andrey').exists():
        CustomUser.objects.create_user(
            username='andrey',
            email='andreytest@test.de',
            password='asdasd',
            type='customer'
        )
        print("Standard-Customer Nutzer 'andrey' wurde für Gäste Login erstellt.")

    if not CustomUser.objects.filter(username='kevin').exists():
        CustomUser.objects.create_user(
            username='kevin',
            email='kevintest@test.de',
            password='asdasd24',
            type='business'
        )
        print("Standard-Business Nutzer 'kevin' wurde für Gäste Login erstellt.")
