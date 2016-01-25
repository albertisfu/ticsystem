from django.apps import AppConfig
from django.db.models.signals import post_migrate

from signals import handlers

class MyAppConfig(AppConfig):
    name = 'customers'
    verbose_name = 'Customers'

    def ready(self):
        post_migrate.connect(handlers.create_notice_types, sender=self)