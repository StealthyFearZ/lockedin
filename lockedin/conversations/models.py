from django.contrib.auth.models import User
from django.db import models

class Message(models.Model):
    
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages',
        null=True, 
        blank=True
    )    

    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_messages',
        null=True,
        blank=True
    )

    #both sender and recipient ensure that each message and convo is unique
    content = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.content[:20]}"