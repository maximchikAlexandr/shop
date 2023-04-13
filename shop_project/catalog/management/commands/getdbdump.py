from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand

from shop_project.settings import BASE_DIR

name_apps = [
    "users",
    "catalog",
]


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        self.models = []
        for app in name_apps:
            for model in apps.get_app_config(app).get_models():
                self.models.append(f"{app}.{model.__name__}")
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        for model in self.models:
            call_command(
                "dumpdata",
                f"--output={BASE_DIR}/catalog/tests/fixtures/{model}.json",
                "--indent=4",
                "--format=json",
                model,
            )

        return "\n".join(self.models)
