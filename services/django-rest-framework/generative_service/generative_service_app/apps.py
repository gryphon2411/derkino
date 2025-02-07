import os

from django.apps import AppConfig


class GenerativeServiceAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'generative_service_app'
    huggingface_hub_access_token = os.getenv("HUGGINGFACE_HUB_ACCESS_TOKEN")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    generative_model_name = os.getenv("GENERATIVE_MODEL_NAME")
    rabbitmq_username = os.getenv("RABBITMQ_USERNAME")
    rabbitmq_password = os.getenv("RABBITMQ_PASSWORD")
    rabbitmq_host_address = os.getenv("RABBITMQ_HOST_ADDRESS")
    rabbitmq_host_port = os.getenv("RABBITMQ_HOST_PORT")
    rabbitmq_vhost = os.getenv("RABBITMQ_VHOST")
