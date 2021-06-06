from django.core.management.base import BaseCommand

from botrunner import BotRunner
from bots.models import Bot, STOPPED


class Command(BaseCommand):
    help = "Run Bot Runner"

    def add_arguments(self, parser):
        parser.add_argument('--port', help="Set Bot Runner Port (default: 5555)", default=5555, type=int)
        parser.add_argument('--debug_logging', help="Enable debug message in log for Bot Runner", default=1, type=int)
        parser.add_argument('--enable_logging', help="Enable logging from Bot Runner", default=1, type=int)

    def handle(self, *args, **options):
        bot_runner = BotRunner(debug_logging=options['debug_logging'], enable_logging=options['enable_logging'])

        try:
            bot_runner.start()
        except KeyboardInterrupt:
            bot_runner.stop()
