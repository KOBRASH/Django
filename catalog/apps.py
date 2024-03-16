from django.apps import AppConfig
from django.contrib.auth.management import create_permissions
from django.db.models.signals import post_migrate


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
    def ready(self):
        post_migrate.connect(create_permissions, sender=self)
