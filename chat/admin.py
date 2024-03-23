from django.contrib import admin
from .models import ChatItem, Story, Charactor

class StoryAdmin(admin.ModelAdmin):
  list_display = ['id', 'title', 'title_description', 'genre', 'classification', 'background']

class CharactorAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'personality', 'greeting', 'story_id_id']

class ChatAdmin(admin.ModelAdmin):
  list_display = [field.name for field in ChatItem._meta.get_fields()]

admin.site.register(Story, StoryAdmin)
admin.site.register(Charactor, CharactorAdmin)
admin.site.register(ChatItem, ChatAdmin)
