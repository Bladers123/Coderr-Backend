from django.apps import AppConfig


class FreelancerPlatformAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'freelancer_platform_app'

    def ready(self):
        pass
        import freelancer_platform_app.api.signals

   