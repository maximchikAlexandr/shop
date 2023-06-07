from typing import Optional

import requests
from django.conf import settings


def get_data_from_api(uri: str, headers: Optional[dict] = None) -> dict:
    url = f"http://{settings.DJANGO_APP_HOST}:{settings.DJANGO_APP_PORT}/{uri}/"
    return requests.get(url, headers=headers, timeout=5).json()
