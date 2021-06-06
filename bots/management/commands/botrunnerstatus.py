from django.core.management.base import BaseCommand
from . import get_status


class Command(BaseCommand):
    help = "Bot Runner Status"

    def add_arguments(self, parser):
        parser.add_argument('--port', help="Set Bot Runner Port (default: 5555)", default=5555, type=int)

    def handle(self, *args, **options):
        resp = get_status(options['port'])
        print(resp)
