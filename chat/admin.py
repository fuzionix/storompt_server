from django.contrib import admin
from .models import ChatItem, Story

class ChatAdmin(admin.ModelAdmin):
  list_display = [field.name for field in ChatItem._meta.get_fields()]

class StoryAdmin(admin.ModelAdmin):
  list_display = ['id', 'title', 'title_description', 'genre', 'classification', 'background']

admin.site.register(ChatItem, ChatAdmin)
admin.site.register(Story, StoryAdmin)
