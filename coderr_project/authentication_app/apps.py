from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication_app'


    def ready(self):
        pass
        import authentication_app.api.signals