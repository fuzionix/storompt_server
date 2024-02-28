from django.contrib import admin
from .models import ChatItem, Story

class ChatAdmin(admin.ModelAdmin):
  list_display_chat = [field.name for field in ChatItem._meta.get_fields()]

class StoryAdmin(admin.ModelAdmin):
  list_display_story = [field.name for field in Story._meta.get_fields()]

admin.site.register(ChatItem, ChatAdmin)
admin.site.register(Story, StoryAdmin)
