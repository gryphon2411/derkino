import os

from django.apps import AppConfig


class GenerativeServiceAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'generative_service_app'
    huggingface_hub_access_token = os.getenv("HUGGINGFACE_HUB_ACCESS_TOKEN")
