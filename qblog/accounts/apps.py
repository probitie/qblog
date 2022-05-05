from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

# creates user profile object automatically when user object is saving to db
    def ready(self):
        from . import signals


default_app_config = 'users.apps.UsersConfig'
