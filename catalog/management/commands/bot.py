from aiogram.utils import executor
from django.core.management.base import BaseCommand

from bot.main import dp


class Command(BaseCommand):
    help = "Test TG Bot"

    def handle(self, *args, **options):
        executor.start_polling(dp)
