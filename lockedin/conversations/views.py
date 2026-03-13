from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message

@login_required
def conversation(request, username):
    other_user = get_object_or_404(User, username=username)

    sent_messages = Message.objects.filter(sender=request.user, recipient=other_user)

    recieved_messages = Message.objects.filter(sender=other_user, recipient=request.user)

    # Combined messages and creates union for them

    messages = sent_messages.union(recieved_messages).order_by('-sent')

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            Message.objects.create(sender=request.user, recipient=other_user, content=content)
            return redirect('conversation.detail', username=username)

    return render(request, 'conversations/conversations_list.html', {
        'other_user': other_user,
        'messages': messages,
    })