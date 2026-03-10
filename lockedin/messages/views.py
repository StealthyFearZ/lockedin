from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Experience, Education

# Profile Views

@login_required
def messages_list(request, username=None):
    # You have to be logged in to view a profile
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    profile, created = Profile.objects.get_or_create(user=user)

    context = {
        'profile' : profile,
        'is_own_profile' : request.user == user,
        'template_data' : {'title' : f"{user.username}'s Profile"}
    }
    return render(request, 'profiles/profile_detail.html', context)