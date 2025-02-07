from logging import getLogger
from typing import Optional

from django.apps import apps
from google import genai
from google.genai import types

gemini2flash_generative_model = None  # type: Optional[Gemini2FlashGenerativeModel]


def get_gemini2flash_generative_model():
    global gemini2flash_generative_model

    if not gemini2flash_generative_model:
        gemini2flash_generative_model = Gemini2FlashGenerativeModel()

    return gemini2flash_generative_model


class Gemini2FlashGenerativeModel:
    MODEL_NAME = "gemini-2.0-flash"
    GEMINI_API_KEY = apps.get_app_config("generative_service_app").gemini_api_key
    TITLE_FACTS_SYSTEM_INSTRUCTION = ("When providing lists of facts or information, present the facts directly "
                                      "without introductory or concluding sentences.")
    TITLE_FACTS_PROMPT_TEMPLATE = "List 3 interesting facts about \"{title_name}\" ({title_year}) {title_type}."

    def __init__(self):
        self._logger = getLogger(self.__class__.__name__)
        self._model_name = self.MODEL_NAME
        self._client = genai.Client(api_key=self.GEMINI_API_KEY)
        self._content_config=types.GenerateContentConfig(system_instruction=self.TITLE_FACTS_SYSTEM_INSTRUCTION)

    def prompt_title_facts(self, title_name, title_year, title_type):
        input_text = self.TITLE_FACTS_PROMPT_TEMPLATE.format(title_name=title_name, title_year=title_year,
                                                             title_type=title_type)

        contents = [input_text]

        self._logger.warning(f"Generating '{self._model_name}' outputs for title facts prompt")

        model_response = self._client.models.generate_content(model=self._model_name, config=self._content_config,
                                                              contents=contents)

        return model_response.text
