from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from generative_service_app.generative_models.gemma import get_gemma_generative_model


class TitleFacts(APIView):
    def post(self, request, format=None):
        title_name = request.data.get('title_name')
        title_year = request.data.get('title_year')

        if not title_name or not title_year:
            return Response(
                {"error": "Both 'title_name' and 'title_year' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        gemma_generative_model = get_gemma_generative_model()

        facts = gemma_generative_model.prompt_title_facts(title_name, title_year)

        return Response({"facts": facts})
