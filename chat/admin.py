from django.contrib import admin
from .models import ChatItem

class ChatAdmin(admin.ModelAdmin):
  list_display = [field.name for field in ChatItem._meta.get_fields()]

admin.site.register(ChatItem, ChatAdmin)