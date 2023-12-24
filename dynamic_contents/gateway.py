# Python
import logging
import requests
from typing import Any
from urllib.parse import urljoin

# Django
from django.conf import settings


# Variables
logger = logging.getLogger(__name__)


# Classes
class BaseGateway:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_url(self, path: str) -> str:
        return urljoin(self.base_url, path)

    def request(self, method: str, path: str, *args, **kwargs) -> Any:
        try:
            response = requests.request(method, self.get_url(path), *args, **kwargs)
        except requests.RequestException as exc:
            # Write logs for possible request errors
            logger.warning(f"Unexpected exception caught: {exc!s}")
            raise

        # Raise exception for HTTP error status codes such as 400, 404, 500.
        # response.raise_for_status()

        return response.json()


class GatewayV1(BaseGateway):
    def __init__(self):
        super().__init__(base_url=urljoin(settings.GATEWAY1_HOST, f'/api/'))

    def func1(self, field_value1: str, field_value2: str):
        path = 'path1/path2/...'

        body = {
            "field_name1": field_value1,
            "field_name2": field_value2,
        }
        print('[func1] body : ', body)

        return self.request(method="POST", path=path, json=body)


# Instances
package_sdk = GatewayV1()
