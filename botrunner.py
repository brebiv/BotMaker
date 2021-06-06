import zmq
import django

import os, sys
import time
import logging
import datetime
from threading import Thread
from multiprocessing import Process

from bots.bot import TelegramBotThread, TelegramBotProcess


def initDjagoORM() -> None:
    # Django ORM init
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'botmaker.settings')
    django.setup()
    from bots.models import Bot, Command
    global Bot, Command


class BotRunner:

    def __init__(self, port=5555, debug_logging=True, enable_logging=True):
        # Configuring logging
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('telegram').setLevel(logging.INFO)  # Disable python-telegram-bot logging
        self.logger = logging.getLogger('botrunner')
        if debug_logging:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        if enable_logging == 0:
            # self.logger.info("Logger is disabled. So no logs anymore. You are probably testing right?")
            logging.disable(logging.CRITICAL)

        initDjagoORM()
        self.logger.debug("Database ready")

        # IPC init
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.bind(f"tcp://127.0.0.1:{port}")
        self.logger.debug("Socket ready")

        # Bots Management init
        self.active_bots = []

        # Process statistics variables
        self.birth_datetime = datetime.datetime.now()
        self.active_bots_count = 0

    def start(self):
        """Starting bot runner. Waiting for command from socket and calling method represented by this commands"""
        self.logger.info("Starting Bot Runner...")
        while True:
            self.logger.debug("Awaiting message...")
            msg = self.socket.recv_json()
            command = msg['command']
            self.logger.debug(f"Got {msg}")
            
            if command == 'get_status':
                self.socket.send_json(self.get_status())
            elif command == 'ping':
                self.socket.send_json({"ping": True})
            elif command == 'start_bot':
                bot_id = msg['bot_id']
                self.socket.send_json(self.start_bot(bot_id))
            elif command == 'stop_bot':
                bot_id = msg['bot_id']
                self.socket.send_json(self.stop_bot(bot_id))
            elif command == 'restart_bot':
                bot_id = msg['bot_id']
                self.socket.send_json(self.restart_bot(bot_id))
            elif command == 'reload':
                self.socket.send_json(self.reload())
            elif command == 'stop':
                self.stop()
            elif command == 'bot_error':
                if msg['bot_error'] == 'BOT_TIMED_OUT':
                    bot_id = msg['bot_id']
                    restart_thread = Thread(target=self.restart_bot, kwargs={'bot_id': bot_id, 'delay': 5})
                    restart_thread.start()
                    # self.restart_bot(bot_id)

    def stop(self):
        """Stopping bot runner. Closing socket."""
        self.logger.info("Stopping Bot Runner...")
        self.socket.close()
        self.context.term()
        for bot in self.active_bots:
            bot.terminate()
        sys.exit()

    def reload(self):
        """Reload database"""
        initDjagoORM()
        return {"message": "Ok"}

    def get_status(self):
        """Returns process statistics. :returns """
        return {"active_bots_count": self.active_bots_count,
                "uptime": str(datetime.datetime.now() - self.birth_datetime),
                "active_bots_ids": [i.db_id for i in self.active_bots],
                "running": True}

    def start_bot(self, bot_id: int):
        """Starting bot processes"""
        for bot in self.active_bots:
            if bot.db_id == bot_id:
                return {"error": "Bot already active"}

        try:
            bot = Bot.objects.get(pk=bot_id)
            commands = [c for c in Command.objects.filter(bot_id=bot_id)]
        except Bot.DoesNotExist:
            return {"error": "Bot with given id DoesNotExist", 'id': bot_id}
        else:
            self.logger.info(f"Starting bot {bot.id}")

            bot_process = TelegramBotProcess(bot.id, bot.token, commands)
            self.active_bots.append(bot_process)
            # self.logger.debug("BEFORE BOT PROCCES")
            bot_process.start()
            # self.logger.debug("AFTER BOT PROCCESS")
            bot.status = 1
            bot.save()
            self.active_bots_count += 1
            return {"message": f"Bot with id {bot_id} started."}

    def stop_bot(self, bot_id: int):
        """Terminate bot process"""
        if bot_id not in [i.db_id for i in self.active_bots]:
            return {"error": f"There is no bot with this id: {bot_id}"}

        for bot in self.active_bots:
            if bot.db_id == bot_id:
                bot.terminate()
                self.active_bots.remove(bot)
                self.active_bots_count -= 1

                db_bot = Bot.objects.get(pk=bot_id)
                db_bot.status = 0
                db_bot.save()
                return {"message": f"Bot with id: {bot_id} successfully stopped"}

    def restart_bot(self, bot_id: int, delay = 0):
        """Restart bot. It will load new commands and might fix network problems"""
        if delay != 0:
            logging.debug(f"[BotRunner] Sleeping {delay} seconds before restarting bot with id: {bot_id}")
            time.sleep(delay)
        logging.debug(f"[BotRunner] Restarting bot with id: {bot_id}")
        if bot_id not in [i.db_id for i in self.active_bots]:
            return {"error": f"There is no bot with this id: {bot_id}"}

        for bot in self.active_bots:
            if bot.db_id == bot_id:
                self.stop_bot(bot_id)
                self.start_bot(bot_id)
                return {"message": f"Bot with id: {bot_id} successfully restarted."}


class BotRunnerProcess(Process):
    def __init__(self, port=5555, debug_logging=True):
        super().__init__()
        self.bot_runner = BotRunner(port, debug_logging)

    def run(self) -> None:
        self.bot_runner.start()

    def start(self) -> None:
        self.bot_runner.start()

    def terminate(self) -> None:
        self.bot_runner.stop()


if __name__ == '__main__':
    # Initializing Bot Runner
    # bot_runner = BotRunner()
    initDjagoORM()

    # try:
    #     bot_runner.start()
    # except KeyboardInterrupt:
    #     bot_runner.stop()

    test_bot = Bot.objects.first()
    commands = Command.objects.filter(bot=test_bot)
    bot_process = TelegramBotProcess(test_bot.id, test_bot.token, commands)
    bot_process.run()
