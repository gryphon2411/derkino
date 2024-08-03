from typing import Optional

from generative_service_app.generative_models.inference_client_chat_completion_generative_model import \
    InferenceClientChatCompletionGenerativeModel

mixtral8x7b_generative_model = None  # type: Optional[Mixtral8x7bGenerativeModel]


def get_mixtral8x7b_generative_model():
    global mixtral8x7b_generative_model

    if not mixtral8x7b_generative_model:
        mixtral8x7b_generative_model = Mixtral8x7bGenerativeModel()

    return mixtral8x7b_generative_model


class Mixtral8x7bGenerativeModel(InferenceClientChatCompletionGenerativeModel):
    MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

    def __init__(self):
        super().__init__(self.MODEL_NAME)
