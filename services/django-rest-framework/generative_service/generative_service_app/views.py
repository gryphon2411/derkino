import requests
from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from generative_service_app.generative_models.gemma import get_gemma_generative_model
from generative_service_app.generative_models.phi3 import get_phi3_generative_model


class TitleFacts(APIView):
    GENERATIVE_MODEL_NAME = apps.get_app_config("generative_service_app").generative_model_name
    DATA_SERVICE_HOST = apps.get_app_config("generative_service_app").data_service_host

    def __init__(self):
        super().__init__()

        self._generative_model = self._get_generative_model()

    def _get_generative_model(self):
        _generative_model = None

        if self.GENERATIVE_MODEL_NAME == "gemma":
            _generative_model = get_gemma_generative_model()
        elif self.GENERATIVE_MODEL_NAME == "phi3":
            _generative_model = get_phi3_generative_model()

        return _generative_model

    def post(self, request, title_id, format=None):
        response = requests.get(f"{self.DATA_SERVICE_HOST}/api/v1/data/titles/{title_id}")
        if response.status_code != 200:
            return Response(
                {"error": f"Unable to fetch title '{title_id}' from data service at {self.DATA_SERVICE_HOST}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        title_name, title_year = self._get_title_name_and_year(response)

        facts = self._generative_model.prompt_title_facts(title_name, title_year)

        return Response({"facts": facts})

    def _get_title_name_and_year(self, response):
        data = response.json()
        title_name = data.get('primaryTitle')

        start_year = data.get('startYear')
        end_year = data.get('endYear')

        title_year = end_year if end_year else start_year

        return title_name, title_year
