from rest_framework.authentication import BaseAuthentication

from users.models import CustomUser


class TelegramAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", None)
        if auth_header is not None and auth_header.startswith("tg_chat_id "):
            chat_id = auth_header.split()[1]
            user = self.get_user(tg_chat_id=chat_id)
            return user, None

    @staticmethod
    def get_user(tg_chat_id):
        try:
            return CustomUser.objects.get(tg_chat_id=tg_chat_id)
        except CustomUser.DoesNotExist:
            return None
