from django.conf import settings
from django.core.management.base import BaseCommand
from user.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        admins = settings.SUPERADMINS
        for email, password in admins:
            if not User.objects.filter(email=email).exists():
                u = User.objects.create_superuser(email=email, password=password)
                u.save()
                print(f"User '{email}' successfully created")
            else:
                print(f"User '{email}' already exists")
