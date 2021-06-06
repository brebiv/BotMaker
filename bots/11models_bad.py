from django.db import models
from django.contrib.auth.models import User
from telegram import Bot as TBot, bot

import requests


class Bot(models.Model):

    class Meta:
        db_table = 'bots'

    id = models.AutoField(primary_key=True, help_text="Database ID")
    tid = models.IntegerField(null=False, unique=True, editable=False, help_text="Telegram API ID")
    token = models.CharField(max_length=46, unique=True, null=False, blank=False, help_text="Telegram API Token")
    username = models.CharField(max_length=64, unique=False, null=False, editable=False)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    STOPPED = 0
    RUNNING = 1

    STATUS_CHOICES = (
        (RUNNING, 'Running'),
        (STOPPED, 'Stopped'),
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=STOPPED)

    @staticmethod
    def check_token(token: str) -> bool:
        response = requests.get(f"https://api.telegram.org/bot{token}/getMe")
        if response.status_code == 200:
            return True
        else:
            raise ValueError("Telegram response status code is not 200 :(")

    def save(self, *args, **kwargs):
        if self.check_token(self.token):
            bot = TBot(token=self.token)
            self.tid = bot.id
            self.username = bot.username
            super(Bot, self).save(*args, **kwargs)

    def as_dict(self):
        data = {
            "id": self.id,
            "tid": self.tid,
            "username": self.username,
            "owner": self.owner.id,
            "created_at": self.created_at,
            "status": self.status
        }
        return data

    def __str__(self):
        return f"<Bot id: {self.id} tid: {self.tid}>"


class InlineKeyboard(models.Model):

    class Meta:
        db_table = 'inline_keyboards'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"<InlineKeyboard name: {self.name}>"


class InlineKeyboardButton(models.Model):

    class Meta:
        db_table = 'inline_keyboard_buttons'
    
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    url = models.URLField(default='', blank=True)
    callback_data = models.CharField(max_length=64, default='', blank=True)
    keyboard = models.ForeignKey(to=InlineKeyboard, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"<InlineKeyboardButton text: {self.text}>"


class ResponseType(models.Model):

    class Meta:
        db_table = 'response_types'
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=128)

    def __str__(self):
        return f"<Response type name: {self.name}>"


class DataSourceType(models.Model):
    
    class Meta:
        db_table = 'data_source_types'
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return f"<DataSourceType name: {self.name}>"


class DataSource(models.Model):

    class Meta:
        db_table = 'data_sources'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, default='', blank=True)
    type = models.ForeignKey(to=DataSourceType, on_delete=models.DO_NOTHING)
    url = models.URLField()

    def __str__(self) -> str:
        return f"<DataSource type: {self.type} url: {self.url}>"


class Command(models.Model):

    class Meta:
        db_table = 'commands'

    id = models.AutoField(primary_key=True)
    response_type = models.ForeignKey(to=ResponseType, on_delete=models.DO_NOTHING, default=1)
    trigger = models.CharField(max_length=128, null=False, help_text="Text which will trigger command")
    reply_text = models.TextField(help_text="Text to be sent when command is triggered", default='', blank=True)
    reply_img_url = models.TextField(help_text="Url to image", default='', blank=True)
    data_source = models.ForeignKey(to=DataSource, on_delete=models.DO_NOTHING, null=True, blank=True)
    inline_keyboard = models.ForeignKey(to=InlineKeyboard, on_delete=models.DO_NOTHING, null=True, blank=True)
    bot = models.ForeignKey(to=Bot, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def as_dict(self):
        return {
            "id": self.id,
            "response_type": self.response_type.id,
            "trigger": self.trigger,
            "reply_text": self.reply_text,
            "reply_img_url": self.reply_img_url,
            "data_source": 0,
            "inline_keyboard": 0,
            "bot": self.bot.id,
            "owner": self.owner.id,
            "created_at": self.created_at,
        }

    def __str__(self):
        return f"<Command trigger: {self.trigger} bot_id: {self.bot_id}>"


class CallbackHandler(models.Model):

    class Meta:
        db_table = 'callback_handlers'

    id = models.AutoField(primary_key=True)
    trigger = models.CharField(max_length=64)
    response_type = models.ForeignKey(to=ResponseType, on_delete=models.DO_NOTHING)
    reply_text = models.TextField(default='', blank=True)
    data_source = models.ForeignKey(to=DataSource, on_delete=models.DO_NOTHING)
    bot = models.ForeignKey(to=Bot, on_delete=models.DO_NOTHING)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "trigger": self.trigger,
            "response_type": self.response_type.name,
            "reply_text": self.reply_text,
            "data_source": 0,
            "bot": self.bot.id,
        }

    def __str__(self) -> str:
        return f"<Callback handler trigger: {self.trigger} response_type: {self.response_type}>"


class Message(models.Model):

    class Meta:
        db_table = 'messages'
    
    id = models.AutoField(primary_key=True)
    bot = models.ForeignKey(to=Bot, on_delete=models.DO_NOTHING)
    sender_tid = models.IntegerField(null=False, editable=False, help_text="Message sender tid")
    text = models.TextField()
    date = models.DateTimeField(verbose_name="Date and time message was sent")

    def as_dict(self):
        return {
            "id": self.id,
            "bot_id": self.bot.id,
            "sender_tid": self.sender_tid,
            "text": self.text,
            "date": self.date,
        }

    def __str__(self):
        return f"<Message sender: {self.sender_tid} date:{self.date}>"
