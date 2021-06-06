from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.views.decorators.csrf import csrf_exempt
from BotMaker.BotRunnerClient import BotRunnerClient
from datetime import datetime

from .serializers import CallbackHandlerSerializer, LoginSerializer, CreateBotSerializer, BotSerializer, CommandSerializer, InlineKeyboardSerializer, MessageSerializer
from bots.models import Command, Bot, InlineKeyboard, InlineKeyboardButton, CallbackHandler, Message


@api_view(['POST'])
@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(email=email, password=password)
            if user is None:
                return JsonResponse({"message": "bad creds"}, status=400)
            login(request, user)
            bot_id = None
            try:
                bot = Bot.objects.get(owner=user)
                bot_id = bot.pk
            except Bot.DoesNotExist:
                pass
            return JsonResponse({"valid": True, "user_id": user.pk, "bot_id": bot_id}, status=200)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
def api_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"status": "ok"}, status=200)
    return JsonResponse({"msg": "You are not logged in"}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bot_list(request):
    if request.method == 'POST':
        # print(request.data)
        serializer = CreateBotSerializer(data=request.data)
        if serializer.is_valid():
            try:
                Bot.objects.get(token=serializer.validated_data.get('token'))
                return JsonResponse({"message": "Bot already exists"}, status=409)
            except Bot.DoesNotExist:
                try:
                    serializer.save()
                    bot_token = serializer.validated_data.get('token')
                    bot = Bot.objects.get(token=bot_token)
                    resp_serializer = BotSerializer(bot)
                    return JsonResponse(resp_serializer.data, status=201)
                except ValueError:
                    return JsonResponse({"msg": "Not valid token"}, status=400)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bot_detail(request, bot_id):
    try:
        bot = Bot.objects.get(pk=bot_id)
    except Bot.DoesNotExist:
        return JsonResponse({"msg": "Bot not found"}, status=404)
        # return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BotSerializer(bot)
        return JsonResponse(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def command_list(request, bot_id):
    """
    List all code commands, or create a new command.
    """
    if request.method == 'GET':
        commands = Command.objects.filter(bot_id=bot_id).all()
        serializer = CommandSerializer(commands, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = CommandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def command_detail(request, command_id):
    """Single command get, put or delete"""
    try:
        command = Command.objects.get(pk=command_id)
    except Command.DoesNotExist:
        return JsonResponse({"msg": "Command not found"}, status=404)

    if request.method == 'GET':
        serializer = CommandSerializer(command)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        serializer = CommandSerializer(command, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        command = Command.objects.get(pk=command_id)
        command.delete()
        return HttpResponse(status=204)


@api_view(['GET', 'POST'])
def inline_keyboards_list(request, bot_id):
    """Inline keyboard list for specific bot"""
    if request.method == 'GET':
        keyboards = InlineKeyboard.objects.filter(bot_id=bot_id).all()
        serializer = InlineKeyboardSerializer(keyboards, many=True)
        # print(serializer)
        # print(serializer.data)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = InlineKeyboardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def callbacks_list(request, bot_id):
    """Return callback handlers"""
    if request.method == 'GET':
        callbacks = CallbackHandler.objects.filter(bot_id=bot_id).all()
        serializer = CallbackHandlerSerializer(callbacks, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = CallbackHandlerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def callback_detail(request, callback_id):
    """Single callback handler CRUD"""
    try:
        callback = CallbackHandler.objects.get(pk=callback_id)
    except Command.DoesNotExist:
        return JsonResponse({"msg": "Callback not found"}, status=404)

    if request.method == 'GET':
        serializer = CallbackHandlerSerializer(callback)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        serializer = CallbackHandlerSerializer(callback, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        callback = CallbackHandler.objects.get(pk=callback_id)
        callback.delete()
        return HttpResponse(status=204)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def messages_list(request, bot_id):
    """List for Message model"""
    if request.method == 'GET':
        date = request.GET['date']
        if date == 'today':
            today = datetime.utcnow().date()
            messages = Message.objects.filter(date__date=today).all()
            serializer = MessageSerializer(messages, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inline_buttons_list(request, command_id):
    """List view for InlineKeyboardButton model"""
    if request.method == 'GET':
        command = Command.objects.filter(pk=command_id)
        print(command)
        print(type(command))




# BotRunner Controlls

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def start_bot(request, bot_id):
    """Start bot with given id"""
    if request.method == 'GET':
        bot_runner_resp = BotRunnerClient().start_bot(bot_id)
        bot = Bot.objects.get(pk=bot_id)
        serializer = BotSerializer(bot)
        return JsonResponse(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stop_bot(request, bot_id):
    """Stop bot"""
    if request.method == 'GET':
        bot_runner_resp = BotRunnerClient().stop_bot(bot_id)
        bot = Bot.objects.get(pk=bot_id)
        serializer = BotSerializer(bot)
        return JsonResponse(serializer.data)
