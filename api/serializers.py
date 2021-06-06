from django.contrib.auth import models
from django.contrib.auth.models import User

from rest_framework import serializers

from bots.models import Bot, Command, InlineKeyboard, InlineKeyboardButton, CallbackHandler, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)


class CreateBotSerializer(serializers.Serializer):

    token = serializers.CharField(max_length=64)
    owner_id = serializers.IntegerField()

    def create(self, validated_data):
        # print("Validated Data:", validated_data)
        # print("TOKENFJEIFJE", validated_data.get('token'))
        # bot = Bot(token=validated_data.get('token'))
        bot = Bot(**validated_data)
        bot.save()
        return bot

    def update(self, instance, validated_data):
        pass


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ['id', 'username', 'created_at', 'status']


class InlineKeyboardButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = InlineKeyboardButton
        fields = ['id', 'text', 'url', 'callback_data']


class InlineKeyboardSerializer(serializers.ModelSerializer):

    buttons = InlineKeyboardButtonSerializer(read_only=True, many=True)

    class Meta:
        model = InlineKeyboard
        depth = 1
        fields = ['id', 'name', 'buttons']


class CommandSerializer(serializers.HyperlinkedModelSerializer):

    bot_id = serializers.IntegerField()
    owner_id = serializers.IntegerField()
    # inline_keyboard = InlineKeyboardSerializer(read_only=True)
    # inline_keyboard_id = serializers.IntegerField(write_only=True, default=None)
    buttons = InlineKeyboardButtonSerializer(many=True)

    class Meta:
        model = Command
        fields = ['id', 'bot_id', 'trigger', 'reply_text', 'reply_img_url', 'buttons', 'owner_id']

    def create(self, validated_data):
        command = Command(
            bot_id=validated_data['bot_id'],
            trigger=validated_data['trigger'],
            reply_text=validated_data['reply_text'],
            reply_img_url=validated_data['reply_img_url'],
            owner_id=validated_data['owner_id']
        )

        # For loop below, will not work in length of buttons is 0
        command.save()
        # print(validated_data['buttons'])
        # for b in validated_data['buttons']:
        #     print(b['text'])
        for b in validated_data['buttons']:
            button = InlineKeyboardButton(text=b['text'], url=b['url'], callback_data=b['callback_data'], command=command)
            button.save()
        # command.buttons.set(validated_data['buttons'])
        return command
    
    def update(self, instance, validated_data):
        instance.trigger = validated_data['trigger']
        instance.reply_text = validated_data['reply_text']
        instance.reply_img_url = validated_data['reply_img_url']
        instance.save()
        return instance


class CallbackHandlerSerializer(serializers.ModelSerializer):

    bot_id = serializers.IntegerField()

    class Meta:
        model = CallbackHandler
        fields = ['id', 'trigger', 'reply_text', 'reply_img_url', 'bot_id']

    def create(self, validated_data):
        callback_handler = CallbackHandler(
            trigger=validated_data['trigger'],
            bot_id=validated_data['bot_id'],
            reply_text=validated_data['reply_text'],
            reply_img_url=validated_data['reply_img_url']
        )

        callback_handler.save()
        return callback_handler


class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ['id', 'text', 'date', 'sender_tid']
