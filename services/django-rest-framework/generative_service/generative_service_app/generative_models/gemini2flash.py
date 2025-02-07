import logging
from typing import Optional

import requests
from django.apps import apps


gemini2flash_generative_model = None  # type: Optional[Gemini2FlashGenerativeModel]


def get_gemini2flash_generative_model():
    global gemini2flash_generative_model

    if not gemini2flash_generative_model:
        gemini2flash_generative_model = Gemini2FlashGenerativeModel()

    return gemini2flash_generative_model


class Gemini2FlashGenerativeModel:
    MODEL_NAME = "gemini-2.0-flash"
    API_KEY = apps.get_app_config("generative_service_app").gemini_api_key
    API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    API_URL = f"{API_BASE_URL}/{MODEL_NAME}:generateContent?key={API_KEY}"
    API_HEADERS = {"Content-Type": "application/json"}
    TITLE_FACTS_SYSTEM_INSTRUCTION = "When listing facts, present the facts without introductory or concluding sentences."
    TITLE_FACTS_PROMPT_TEMPLATE = "List 3 interesting facts about \"{title_name}\" ({title_year}) {title_type}."

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def prompt_title_facts(self, title_name, title_year, title_type):
        input_text = self.TITLE_FACTS_PROMPT_TEMPLATE.format(title_name=title_name, title_year=title_year,
                                                             title_type=title_type)

        data = {
            "system_instruction": {
                "parts": {
                    "text": self.TITLE_FACTS_SYSTEM_INSTRUCTION
                }
            },
            "contents": {
                "parts": {
                    "text": input_text
                }
            }
        }

        self._logger.warning(f"Generating '{self.MODEL_NAME}' outputs for title facts prompt...")

        model_response = "Try again later..."

        try:
            response = requests.post(self.API_URL, headers=self.API_HEADERS, json=data)
            response.raise_for_status()
            response_json = response.json()

            model_response = response_json["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            self._logger.exception(f"Failed to request title facts for \"{title_name}\" ({title_year}) {title_type}")

        return model_response
