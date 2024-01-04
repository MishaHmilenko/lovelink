from django.db import models

from users.models import User


class Chat(models.Model):
    members = models.ManyToManyField(User, related_name='members')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return f'User: {self.user} -> Chat: {self.chat}'
