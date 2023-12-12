from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Chat(models.Model):
    name = models.CharField(
        max_length=255, null=False, blank=False, unique=True
    )
    host = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chats"
    )
    current_users = models.ManyToManyField(
        User, related_name="current_rooms", blank=True
    )

    def __str__(self):
        return f"Chat({self.name} {self.host})"


class Message(models.Model):
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="messages"
    )
    text = models.TextField(max_length=500)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    received = models.BooleanField(
        verbose_name="Статус прочитано", default=False
    )

    def __str__(self):
        return f"Message({self.user} {self.chat})"
