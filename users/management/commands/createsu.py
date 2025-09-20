from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Створює суперкористувача автоматично, якщо його ще немає"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(user_name="admin").exists():
            User.objects.create_superuser(
                user_name="admin",
                email="admin@example.com",
                password=os.environ.get("DJANGO_SUPERUSER_PASSWORD", "holypython123"),
            )
            self.stdout.write(self.style.SUCCESS("Суперкористувача створено успішно."))
        else:
            self.stdout.write("Суперкористувач вже існує")