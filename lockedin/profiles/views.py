from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.
@login_required
def profile_view(request, username=None):
    # You have to be logged in to view a profile
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    profile, created = Profile.objects.get_or_create(user=user)

    context = {
        'profile' : profile,
        'is_their_profile' : request.user == user,
        'template_data' : {'profile_name' : f"{user.username}'s Profile"}
    }
    return render(request, 'profiles/profile_detail.html', context)