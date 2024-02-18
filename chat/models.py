import uuid
from django.db import models
from django.utils.timezone import now

class ChatItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField()
    title_description = models.TextField(blank=True)
    chat_history = models.JSONField(null=True, blank=True)
    genre = models.TextField(blank=True)
    classification = models.TextField(blank=True)
    background = models.TextField(blank=True)
    create_date = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return self.title
