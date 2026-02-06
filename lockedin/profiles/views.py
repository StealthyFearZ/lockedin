from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm

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

@login_required
def profile_edit(request):
    # Create / Update Profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated')
            return redirect('profiles:profile_detail', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form' : form,
        'profile' : profile,
        'template_data' : {'title' : 'Edit Profile'}
    }
    return render(request, 'profiles/profile_form.html', context)