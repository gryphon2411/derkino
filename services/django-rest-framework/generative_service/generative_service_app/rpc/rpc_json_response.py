import json
from dataclasses import dataclass

from pika.spec import BasicProperties


@dataclass(frozen=True)
class RpcJsonResponse:
    properties: BasicProperties
    body: bytes

    def json(self):
        return json.loads(self.body)
