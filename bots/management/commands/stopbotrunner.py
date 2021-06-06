from django.core.management.base import BaseCommand
from . import stop


class Command(BaseCommand):

    help = "Stop Bot Runner"

    def add_arguments(self, parser):
        parser.add_argument('--port', help="Set Bot Runner Port (default: 5555)", default=5555, type=int)

    def handle(self, *args, **options):
        self.stdout.write("Sending command....")
        stop(options['port'])
        self.stdout.write("Command sent.")
