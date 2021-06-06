from django.db import models
from django.contrib.auth.models import User

from api.models import CustomUser

from telegram import Bot as TBot
import requests

STOPPED = 0
RUNNING = 1

BOT_STATUS_CHOICES = (
        (RUNNING, 'Running'),
        (STOPPED, 'Stopped'),
)


class Bot(models.Model):

    class Meta:
        db_table = 'bots'

    id = models.AutoField(primary_key=True, help_text="Database ID")
    tid = models.IntegerField(null=False, unique=True, editable=False, help_text="Telegram API ID")
    # Change editable to False for token in prod
    token = models.CharField(max_length=46, unique=True, null=False, blank=False, editable=True, help_text="Telegram API Token")
    username = models.CharField(max_length=64, unique=False, null=False, editable=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(choices=BOT_STATUS_CHOICES, default=STOPPED)

    @staticmethod
    def check_token(token: str) -> bool:
        print(token)
        response = requests.get(f"https://api.telegram.org/bot{token}/getMe")
        if response.status_code == 200:
            return True
        else:
            print(response.status_code)
            raise ValueError("Telegram response status code is not 200 :(")

    def save(self, *args, **kwargs):
        print("ARGS", args)
        print("KWARGS", kwargs)
        if self.check_token(self.token):
            bot = TBot(token=self.token)
            self.tid = bot.id
            self.username = bot.username
            super(Bot, self).save(*args, **kwargs)

    def __str__(self):
        return f"<Bot id: {self.id} tid: {self.tid}>"


class InlineKeyboard(models.Model):

    class Meta:
        db_table = 'inline_keyboards'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='', blank=True)
    bot = models.ForeignKey(to=Bot, on_delete=models.DO_NOTHING, default=None, null=True, blank=True)

    def __str__(self) -> str:
        return f"<InlineKeyboard name: {self.name}>"

#class Response()


class Command(models.Model):

    class Meta:
        db_table = 'commands'

    id = models.AutoField(primary_key=True)
    # response_type = models.ForeignKey(to=ResponseType, on_delete=models.DO_NOTHING, default=1)
    trigger = models.CharField(max_length=128, null=False, help_text="Text which will trigger command")
    reply_text = models.TextField(help_text="Text to be sent when command is triggered", default='', blank=True)
    reply_img_url = models.TextField(help_text="Url to image", default='', blank=True)
    reply_json_url = models.URLField(help_text="Url to json data", default='', blank=True)
    # data_source = models.ForeignKey(to=DataSource, on_delete=models.DO_NOTHING, null=True, blank=True)
    # inline_keyboard = models.ForeignKey(to=InlineKeyboard, on_delete=models.DO_NOTHING, null=True, blank=True)
    bot = models.ForeignKey(to=Bot, on_delete=models.DO_NOTHING, null=False)
    owner = models.ForeignKey(to=CustomUser, on_delete=models.DO_NOTHING, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"<Command trigger: {self.trigger} bot_id: {self.bot_id}>"


class InlineKeyboardButton(models.Model):
    class Meta:
        db_table = 'inline_keyboard_buttons'

    id = models.AutoField(primary_key=True)
    text = models.TextField()
    url = models.URLField(default='', blank=True)
    callback_data = models.CharField(max_length=64, default='', blank=True)
    # keyboard = models.ForeignKey(to=InlineKeyboard, on_delete=models.DO_NOTHING, related_name='buttons')
    command = models.ForeignKey(to=Command, on_delete=models.CASCADE, related_name='buttons')

    def __str__(self) -> str:
        return f"<InlineKeyboardButton text: {self.text}>"


class CallbackHandler(models.Model):

    class Meta:
        db_table = 'callback_handlers'

    id = models.AutoField(primary_key=True)
    trigger = models.CharField(max_length=64)
    reply_text = models.TextField(default='', blank=True)
    reply_img_url = models.TextField(help_text="Url to image", default='', blank=True)
    # data_source = models.ForeignKey(to=DataSource, on_delete=models.DO_NOTHING)
    bot = models.ForeignKey(to=Bot, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"<Callback handler trigger: {self.trigger} reply_img_url: {self.reply_img_url}>"


class Message(models.Model):

    class Meta:
        db_table = 'messages'

    id = models.AutoField(primary_key=True)
    bot = models.ForeignKey(to=Bot, on_delete=models.DO_NOTHING, editable=False)
    sender_tid = models.IntegerField(null=False, editable=False, help_text="Message sender tid",)
    text = models.TextField(editable=False)
    date = models.DateTimeField(verbose_name="Date and time message was sent", editable=False)

    def __str__(self):
        return f"<Message sender: {self.sender_tid} date:{self.date}>"