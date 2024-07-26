from logging import getLogger
from typing import Optional

from django.apps import apps
from huggingface_hub import InferenceClient

logger = getLogger(__name__)
phi3_generative_model = None  # type: Optional[Phi3GenerativeModel]


def get_phi3_generative_model():
    global phi3_generative_model

    if not phi3_generative_model:
        phi3_generative_model = Phi3GenerativeModel()

    return phi3_generative_model


class Phi3GenerativeModel:
    ACCESS_TOKEN = apps.get_app_config("generative_service_app").huggingface_hub_access_token
    MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
    TITLE_FACTS_PROMPT_TEMPLATE = ("List shortly 3 interesting facts "
                                   "about \"{title_name}\" ({title_year}).")

    def __init__(self):
        self._inference_client = InferenceClient(self.MODEL_NAME, token=self.ACCESS_TOKEN)

    def prompt_title_facts(self, title_name, title_year):
        input_text = self.TITLE_FACTS_PROMPT_TEMPLATE.format(title_name=title_name, title_year=title_year)

        messages = [
            {"role": "user", "content": input_text},
        ]

        logger.warning(f"Generating '{self.MODEL_NAME}' outputs for title facts prompt...")

        model_response = ""

        for message in self._inference_client.chat_completion(messages=messages, max_tokens=500, stream=True):
            model_response += message.choices[0].delta.content

        return model_response
