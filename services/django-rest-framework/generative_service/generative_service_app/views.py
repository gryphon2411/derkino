from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from generative_service_app.generative_models.gemma import get_gemma_generative_model
from generative_service_app.generative_models.phi3 import get_phi3_generative_model


class TitleFacts(APIView):
    def __init__(self):
        super().__init__()

        self._generative_model = self._get_generative_model()

    def _get_generative_model(self):
        _generative_model = None
        generative_model_name = apps.get_app_config("generative_service_app").generative_model_name

        if generative_model_name == "gemma":
            _generative_model = get_gemma_generative_model()
        elif generative_model_name == "phi3":
            _generative_model = get_phi3_generative_model()

        return _generative_model

    def post(self, request, format=None):
        title_name = request.data.get('title_name')
        title_year = request.data.get('title_year')

        if not title_name or not title_year:
            return Response(
                {"error": "Both 'title_name' and 'title_year' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        facts = self._generative_model.prompt_title_facts(title_name, title_year)

        return Response({"facts": facts})
