from django.db import models
from models import User

# Create your models here.
class Conversation(models.Model):
    messengers = models.ManyToManyField(User, related_name="conversations")
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "conversation"
    
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.textField()
    sent_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content