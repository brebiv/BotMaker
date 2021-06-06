# from bots.models.py import Command
from typing import cast
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, bot
from telegram.error import TimedOut
import django
import zmq
from typing import List
import os

from queue import Queue
import threading
import multiprocessing
import time
import requests
from io import BytesIO
import re

import logging


def initDjagoORM() -> None:
    # Django ORM init
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'botmaker.settings')
    django.setup()
    from bots.models import Bot, Command, Message, CallbackHandler
    from bots.models import InlineKeyboard as InlineKeyboardModel
    from bots.models import InlineKeyboardButton as InlineKeyboardButtonModel
    global Bot, Command, Message, InlineKeyboardModel, InlineKeyboardButtonModel, CallbackHandler


def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs


DEFAULT_BOTRUNNER_PORT = 5555


class TelegramBot(Bot):

    def __init__(self, did: int, token: str, commands: list, polling_timeout=3):
        # Initializing bot instance from python-telegram-bot
        super().__init__(token)
        self.database_id = did
        self.action_commands = commands
        self.updates_queue = Queue()
        self.last_processed_update = 0
        self.polling_timeout = polling_timeout

    def start_polling(self):
        """Getting updates from Telegram servers"""
        while True:
            try:
                updates = self.get_updates(offset=self.last_processed_update)
                # print(updates)
                if not updates:
                    time.sleep(self.polling_timeout)
                else:
                    print(len(updates))
                    self.handle_updates(updates)
            except TimedOut:
                logging.error(f"Bot with database id: {self.database_id} timed out. Sending suicide command...")
                context = zmq.Context()
                socket = context.socket(zmq.PAIR)
                socket.connect(f"tcp://127.0.0.1:{DEFAULT_BOTRUNNER_PORT}")
                socket.send_json({"command": "bot_error", "bot_error": "BOT_TIMED_OUT", "bot_id": self.database_id})
                # resp = socket.recv_json()
                # time.sleep(5)
            # except Exception as err:
            #     logging.error(err)
            #     logging.error(f"Bot with database id: {self.database_id} has unknown error. Sending suicide command...")
            #     context = zmq.Context()
            #     socket = context.socket(zmq.PAIR)
            #     socket.connect(f"tcp://127.0.0.1:{DEFAULT_BOTRUNNER_PORT}")
            #     socket.send_json({"command": "bot_error", "bot_error": "BOT_TIMED_OUT", "bot_id": self.database_id})

    def handle_updates(self, updates):
        """Handling updates received from start_polling method via updates_queue"""
        for update in updates:
            if update.callback_query:
                self._handle_callback_query(update)
                return
            sender_chat_id = update.effective_user.id
            message_text = update.message.text

            # If message is not text. img, audio, sticker, document, etc.
            if (message_text == None):
                self.last_processed_update = update.update_id + 1
                message_text = ''

            for command in self.action_commands:
                if re.match(rf'^{command.trigger}$', message_text):
                    print(command.trigger)
                    inline_keyboard = []
                    # if command.inline_keyboard:
                    #     buttons = InlineKeyboardButtonModel.objects.filter(keyboard=command.inline_keyboard)
                    #     tg_buttons = [InlineKeyboardButton(b.text, callback_data=b.callback_data, url=b.url) for b in buttons]
                    #     # inline_keyboard = [[InlineKeyboardButton(b.text, callback_data='test') for b in buttons]]
                    #     inline_keyboard = split(tg_buttons, 5)
                    #     print(inline_keyboard)
                    #     print(buttons)

                    # if len(command.buttons.all()) > 0:
                        # for b in buttons

                    tg_buttons: List[InlineKeyboardButton] = []
                    for b in command.buttons.all():
                        tg_buttons.append(InlineKeyboardButton(b.text, callback_data=b.callback_data, url=b.url))
                        inline_keyboard = split(tg_buttons, 5)
                        print(inline_keyboard)

                    keyboard_markup = None
                    if len(inline_keyboard) > 0:
                        keyboard_markup = InlineKeyboardMarkup(inline_keyboard)

                    # if command.response_type.name == 'image':

                    if command.reply_img_url != '':
                        print("DOWNLOADING IMAGE")
                        img = BytesIO(requests.get(command.reply_img_url).content)
                        print("IMAGE DOWNLOADED")
                        # print(type(command.reply_text))
                        caption = None
                        if command.reply_text != '':
                            caption = command.reply_text
                        # print(caption)
                        self.send_photo(sender_chat_id, img, caption=caption, reply_markup=keyboard_markup)
                        logging.debug(f"Bot sent image to {sender_chat_id}")
                        # continue
                    elif command.reply_img_url == '':
                        self.send_message(sender_chat_id, command.reply_text, reply_markup=keyboard_markup)
                        # continue
            self.last_processed_update = update.update_id + 1
            # print(Bot.objects.all())
            message = Message(sender_tid=sender_chat_id, text=message_text, date=update.message.date, bot_id=self.database_id)
            message.save()
    
    def _handle_callback_query(self, update):
        print("Handling callback query")
        callback = update.callback_query
        # print(callback)
        sender_chat_id = callback.message.chat.id
        callback_handlers = CallbackHandler.objects.filter(bot__id=self.database_id)
        for handler in callback_handlers:
            if handler.trigger == callback.data:
                if handler.reply_img_url != '':
                    logging.debug(f"[Callback query handler] DOWNLOADING IMAGE {handler.reply_img_url}")
                    img = BytesIO(requests.get(handler.reply_img_url).content)
                    logging.debug("[Callback query handler] IMAGE DOWNLOADED")
                    caption = None
                    if handler.reply_text != '':
                        caption = handler.reply_text
                    self.send_photo(sender_chat_id, img, caption=caption)
                    logging.debug(f"[Callback query handler] Bot sent image to {sender_chat_id}")
                elif handler.reply_img_url == '':
                    self.send_message(sender_chat_id, handler.reply_text)
        self.last_processed_update = update.update_id + 1

    def start(self):
        """Starts polling"""
        self.start_polling()


class TelegramBotThread(threading.Thread):

    def __init__(self, did: int, token: str, commands: list, polling_timeout=3):
        threading.Thread.__init__(self)
        self.bot_database_id = did
        self.bot = TelegramBot(did, token, commands, polling_timeout)

    def run(self) -> None:
        self.bot.start()


class TelegramBotProcess(multiprocessing.Process):

    def __init__(self, did: int, token: str, commands: list, polling_timeout=3):
        super().__init__()
        self.db_id = did
        self.bot = TelegramBot(did, token, commands, polling_timeout)
        print("initing django orm")
        initDjagoORM()

    def run(self) -> None:
        self.bot.start()

