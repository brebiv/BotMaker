from django.contrib import admin
from .models import Bot, Command, Message, InlineKeyboard, InlineKeyboardButton, CallbackHandler


admin.site.register(Bot)
# admin.site.register(ResponseType)
admin.site.register(Command)
admin.site.register(Message)
admin.site.register(InlineKeyboard)
admin.site.register(InlineKeyboardButton)
# admin.site.register(DataSourceType)
# admin.site.register(DataSource)
admin.site.register(CallbackHandler)
