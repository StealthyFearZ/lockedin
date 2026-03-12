from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message

@login_required
def conversation(request, username):
    other_user = get_object_or_404(User, username=username)

    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user)) |
        (Q(sender=other_user) & Q(recipient=request.user))
    ).order_by('sent_time')  # chronological

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            Message.objects.create(sender=request.user, recipient=other_user, content=content)
            return redirect('conversation.detail', username=username)

    return render(request, 'conversations/conversations_list.html', {
        'other_user': other_user,
        'messages': messages,
    })