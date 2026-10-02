from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Project, ProjectMembership


class Command(BaseCommand):
    """Create deterministic users, projects, and memberships for local testing."""

    help = "Create or update sample data for local development."

    def add_arguments(self, parser):
        """Register credential options for the seeded users."""

        parser.add_argument(
            "--admin-password",
            default="admin12345",
            help="Password for the seeded admin user (default: admin12345).",
        )
        parser.add_argument(
            "--demo-password",
            default="demo12345",
            help="Password for the seeded demo user (default: demo12345).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        """Create or update the local development data set."""

        user_model = get_user_model()
        admin_user = self._upsert_user(
            user_model=user_model,
            username="admin",
            email="admin@example.com",
            password=options["admin_password"],
            is_staff=True,
            is_superuser=True,
        )
        demo_user = self._upsert_user(
            user_model=user_model,
            username="demo",
            email="demo@example.com",
            password=options["demo_password"],
            is_staff=False,
            is_superuser=False,
        )

        projects = [
            ("Requirements Management", ProjectMembership.Role.EDITOR),
            ("Demo Project", ProjectMembership.Role.VIEWER),
        ]
        for project_name, demo_role in projects:
            project, _ = Project.objects.get_or_create(name=project_name)
            ProjectMembership.objects.update_or_create(
                project=project,
                user=admin_user,
                defaults={"role": ProjectMembership.Role.OWNER},
            )
            ProjectMembership.objects.update_or_create(
                project=project,
                user=demo_user,
                defaults={"role": demo_role},
            )

        self.stdout.write(self.style.SUCCESS("Development data is ready."))
        self.stdout.write("Admin login: admin / the supplied admin password")
        self.stdout.write("Demo login: demo / the supplied demo password")

    @staticmethod
    def _upsert_user(
        *,
        user_model,
        username: str,
        email: str,
        password: str,
        is_staff: bool,
        is_superuser: bool,
    ):
        """Create or update one seeded user and its local credentials."""

        user, _ = user_model.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        user.email = email
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save()
        return user
