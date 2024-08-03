from typing import Optional

from generative_service_app.generative_models.inference_client_chat_completion_generative_model import \
    InferenceClientChatCompletionGenerativeModel

phi3_generative_model = None  # type: Optional[Phi3GenerativeModel]


def get_phi3_generative_model():
    global phi3_generative_model

    if not phi3_generative_model:
        phi3_generative_model = Phi3GenerativeModel()

    return phi3_generative_model


class Phi3GenerativeModel(InferenceClientChatCompletionGenerativeModel):
    MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"

    def __init__(self):
        super().__init__(self.MODEL_NAME)
