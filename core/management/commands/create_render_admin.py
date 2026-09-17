import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the Render admin user from environment variables if it does not exist."

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME")
        email = os.environ.get("ADMIN_EMAIL")
        password = os.environ.get("ADMIN_PASSWORD")

        if not all((username, email, password)):
            self.stdout.write("Admin environment variables are not set; skipping admin creation.")
            return

        user_model = get_user_model()
        user = user_model.objects.filter(username=username).first()
        if user:
            if not user.is_staff or not user.is_superuser:
                user.is_staff = True
                user.is_superuser = True
                user.save(update_fields=["is_staff", "is_superuser"])
            self.stdout.write(f"Admin user '{username}' already exists.")
            return

        user_model.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS(f"Admin user '{username}' created."))
