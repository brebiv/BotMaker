from django.test import TestCase
from django.core.management import call_command

import bots.management.commands as commands
from bots.models_bad import Bot, Command
from django.contrib.auth.models import User
from botrunner import BotRunnerProcess

from multiprocessing import Process
import multiprocessing

MakeMeFeelDestroyedToken = '1017323371:AAGQJKz7fbQC5eToxNIpvySvbazPpebNhfA'


class BotRunnerTests(TestCase):

    def setUp(self):
        User.objects.create(email='test@test.com')
        Bot.objects.create(token=MakeMeFeelDestroyedToken, owner_id=1)
        self.bot_runner_process = Process(target=call_command, args=('runbotrunner',),
                                          kwargs={'debug_logging': 0, 'enable_logging': 0}, name="Bot Runner Main Process")
        self.bot_runner_process.start()

    def tearDown(self):
        commands.stop()

    def test_bot_runner_is_running(self):
        """Test that Bot Runner process is running"""
        resp = commands.ping()
        self.assertEqual(resp['ping'], True)

    def test_start_bot(self):
        """Test that Bot Runner process can start bot"""
        resp = commands.start_bot(1)
        status_resp = commands.get_status()
        self.assertEqual(resp['message'], 'Bot with id 1 started.')
        self.assertEqual(status_resp['active_bots_count'], 1)

    def test_stop_bot(self):
        """Test that Bot Runner can stop bot"""
        # Start bot
        commands.start_bot(1)
        # Stop that bot
        resp = commands.stop_bot(1)
        status_resp = commands.get_status()
        self.assertEqual(resp['message'], 'Bot with id: 1 successfully stopped')
        self.assertEqual(status_resp['active_bots_count'], 0)

    def test_restart_bot(self):
        """Test that Bot Runner can restart bot"""
        # Start bot
        commands.start_bot(1)
        # Restart that bot
        resp = commands.restart_bot(1)
        status_resp = commands.get_status()
        self.assertEqual(resp['message'], 'Bot with id: 1 successfully restarted.')
        self.assertEqual(status_resp['active_bots_count'], 1)
