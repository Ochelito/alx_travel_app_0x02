from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing
from decimal import Decimal

User = get_user_model()

SAMPLE_LISTINGS = [
    {"title": "Sunny Studio", "description": "Cozy spot near park", "price_per_night": Decimal("59.00"), "max_guests": 2},
    {"title": "City Loft", "description": "Downtown loft w/ skyline view", "price_per_night": Decimal("120.00"), "max_guests": 4},
    {"title": "Beach Cottage", "description": "Steps from the sand", "price_per_night": Decimal("200.00"), "max_guests": 6},
]

class Command(BaseCommand):
    help = "Seed the database with sample listings"

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete existing data before seeding")

    def handle(self, *args, **options):
        if options["reset"]:
            Listing.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared listings"))

        host, _ = User.objects.get_or_create(username="host1", defaults={"email": "host1@example.com"})
        created = 0
        for data in SAMPLE_LISTINGS:
            obj, was_created = Listing.objects.get_or_create(title=data["title"], defaults={**data, "host": host})
            created += 1 if was_created else 0
        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created {created} listings."))
