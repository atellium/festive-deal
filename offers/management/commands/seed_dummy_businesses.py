from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from offers.models import Business, Location


class Command(BaseCommand):
    help = 'Create dummy businesses assigned across the first six locations.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of dummy businesses to create. Defaults to 50.',
        )
        parser.add_argument(
            '--location-count',
            type=int,
            default=6,
            help='Number of locations to use. Defaults to 6.',
        )

    def handle(self, *args, **options):
        count = options['count']
        location_count = options['location_count']
        locations = list(Location.objects.all()[:location_count])

        if len(locations) < location_count:
            raise CommandError(
                f'Expected {location_count} locations, found {len(locations)}.'
            )

        created_count = 0

        with transaction.atomic():
            for index in range(1, count + 1):
                name = f'Dummy Business {index}'
                slug = self.get_unique_slug(name)

                business = Business.objects.create(
                    name=name,
                    slug=slug,
                    address=f'{index} Market Road, Local Area',
                    phone=f'900000{index:04d}',
                    phone_alt=f'910000{index:04d}',
                    whatsapp=f'920000{index:04d}',
                    website=f'https://dummy-business-{index}.example.com',
                    fb_url=f'https://facebook.com/dummybusiness{index}',
                    ig_url=f'https://instagram.com/dummybusiness{index}',
                    is_active=True,
                    is_verified=index % 3 == 0,
                    is_paid=index % 5 == 0,
                )

                primary_location = locations[(index - 1) % len(locations)]
                secondary_location = locations[index % len(locations)]
                business.locations.set({primary_location, secondary_location})
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Created {created_count} dummy businesses.')
        )

    def get_unique_slug(self, name):
        base_slug = slugify(name)
        slug = base_slug
        counter = 2

        while Business.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1

        return slug
