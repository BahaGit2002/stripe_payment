from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        username = "admin"
        email = "admin@example.com"
        password = "admin"

        if not username or not password:
            self.stdout.write("Superuser env vars not set")
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write("Superuser already exists")
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write("Superuser created")
