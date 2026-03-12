from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Conversation, Message

# Profile Views

@login_required
def conversations_list(request, username=None):
    # You have to be logged in to view a profile
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    conversations = Conversation.objects.all().filter(messengers=user).order_by('-updated_time')

    template_data = {}
    template_data['conversations'] = conversations
    return render(request, 'conversations/conversations_list.html', template_data)