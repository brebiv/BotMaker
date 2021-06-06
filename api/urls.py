from django.urls import path

from . import views


# !!!!! FORBID CREATING SAME TRIGGERS FOR COMMANDS

urlpatterns = [
    path('login/', views.api_login, name="Session login from ajax"),
    path('logout/', views.api_logout, name="Session logout from ajax"),
    path('bots/', views.bot_list, name="Create bot"),
    path('bots/<int:bot_id>/', views.bot_detail, name="Bot detail"),
    path('bots/<int:bot_id>/commands/', views.command_list, name="Command list"),
    path('commands/<int:command_id>/', views.command_detail, name="Command detail"),
    path('commands/<int:command_id>/inline_buttons/', views.inline_buttons_list, name="List for InlineKeyboardButton"),
    path('bots/<int:bot_id>/inline_keyboards/', views.inline_keyboards_list, name="List InlineKeyboards for bot"),
    path('bots/<int:bot_id>/callbacks/', views.callbacks_list, name="List CallbackHandlers for bot"),
    path('callbacks/<int:callback_id>/', views.callback_detail, name="CallbackHandler detail"),
    path('bots/<int:bot_id>/messages/', views.messages_list, name="List for Message model"),

    # BotRunner controls
    path('bots/<int:bot_id>/start/', views.start_bot, name="Start bot"),
    path('bots/<int:bot_id>/stop/', views.stop_bot, name="Stop bot"),
]
