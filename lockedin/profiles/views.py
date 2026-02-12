from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Experience
from .forms import ProfileForm, ExperienceForm

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
        'is_own_profile' : request.user == user,
        'template_data' : {'title' : f"{user.username}'s Profile"}
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
            return redirect('profiles.detail', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form' : form,
        'profile' : profile,
        'template_data' : {'title' : 'Edit Profile'}
    }
    return render(request, 'profiles/profile_form.html', context)

@login_required
def add_experience(request):
    # Add new Experience
    # Get Associated Profile
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            work_exp = form.save(commit=False)
            work_exp.profile = profile
            work_exp.save()
            messages.success(request, 'Added Experience!')
            return redirect('profiles.detail', username=request.user.username)
    else:
            form = ExperienceForm()

    context = {
        'form' : form,
        'title' : 'Add Experience',
        'template_data' : {'title', 'Add Experience'}
    }
    return render(request, 'profiles/experience_form.html', context)

@login_required
def edit_experience(request, exp_id):
    # Edit old Experience
    # Get Associated Experience
    work_exp = get_object_or_404(Experience, pk=exp_id, profile__user=request.user)

    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=work_exp)
        if form.is_valid():
            form.save()
            messages.success(request, "Experience Updated!")
            return redirect('profiles.detail', username=request.user.username)
    else:
        form = ExperienceForm(instance=work_exp)

    context = {
        'form' : form,
        'work_exp' : work_exp,
        'title' : 'Edit Experience',
        'template_data' : {'title': 'Edit Experience'}
    }
    return render(request, 'profiles/experience_form.html', context)


@login_required
def delete_experience(request, exp_id):
    # Delete old Experience
    # Get Associated Experience
    work_exp = get_object_or_404(Experience, pk=exp_id, profile__user=request.user)

    if request.method == 'POST':
        work_exp.delete()
        messages.success(request, 'Experience Deleted!')
        return redirect('profiles.detail', username=request.user.username)
    
    context = {
        'work_exp' : work_exp,
        'template_data' : {'title' : 'Delete Experience'}
    }
    return render(request, 'profiles/experience_delete.html', context)