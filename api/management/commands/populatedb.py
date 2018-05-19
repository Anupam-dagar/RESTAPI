from django.core.management.base import BaseCommand
from api.dbfactories import BookingFactory, PriceFactory

class Command(BaseCommand):
    help = 'Seeds the database.'

    def add_arguments(self, parser):
        parser.add_argument('--users',
            default=30,
            type=int,
            help='The number of fake users to create.')

    def handle(self, *args, **options):
        for _ in range(options['users']):
            PriceFactory.create()