import requests
from asgiref.sync import sync_to_async
from django.conf import settings

from users.models import CustomUser


def get_data_from_api(uri: str) -> dict:
    url = f"http://{settings.DJANGO_APP_HOST}:{settings.DJANGO_APP_PORT}/{uri}/"
    return requests.get(url).json()


@sync_to_async
def get_user_by_chat_id(tg_chat_id: int) -> CustomUser:
    return CustomUser.objects.get(tg_chat_id=tg_chat_id)
