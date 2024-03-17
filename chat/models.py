import uuid
from django.db import models
from django.utils.timezone import now
    
class Story(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    title = models.TextField(max_length=100)
    title_description = models.TextField(max_length=200, blank=True)
    genre = models.TextField(max_length=50, blank=True)
    classification = models.TextField(max_length=50, blank=True)
    background = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return str(self.id)
    
class Charactor(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.TextField(max_length=100)
    personality = models.TextField(max_length=1000, blank=True)
    story_id = models.ForeignKey('Story', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
    
class ChatItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_history = models.JSONField(null=True, blank=True)
    create_date = models.DateTimeField(default=now, blank=True)
    story_id = models.ForeignKey('Story', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.id.hex
