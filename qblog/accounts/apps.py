from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

# add this function
    def ready(self):
        from . import signals


# users/__init__.py
default_app_config = 'users.apps.UsersConfig'
