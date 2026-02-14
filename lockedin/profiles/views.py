from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Experience, Education
from .forms import ProfileForm, ExperienceForm, EducationForm

# Profile Views

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
def profile_list(request):
    # View all the profiles, sort currently by time of creation
    profiles = Profile.objects.select_related('user').all().order_by('-time_created')
    
    context = {
        'profiles': profiles,
        'template_data': {'title': 'Browse Profiles'}
    }
    return render(request, 'profiles/profile_list.html', context)

# Experience Views

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

# Education Views

@login_required
def add_education(request):
    # Add new Education
    # Get Associated Profile
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            edu_exp = form.save(commit=False)
            edu_exp.profile = profile
            edu_exp.save()
            messages.success(request, 'Added Education!')
            return redirect('profiles.detail', username=request.user.username)
    else:
            form = EducationForm()

    context = {
        'form' : form,
        'title' : 'Add Education',
        'template_data' : {'title', 'Add Education'}
    }
    return render(request, 'profiles/education_form.html', context)

@login_required
def edit_education(request, exp_id):
    # Edit old Education
    # Get Associated Education
    edu_exp = get_object_or_404(Education, pk=exp_id, profile__user=request.user)

    if request.method == 'POST':
        form = EducationForm(request.POST, instance=edu_exp)
        if form.is_valid():
            form.save()
            messages.success(request, "Education Updated!")
            return redirect('profiles.detail', username=request.user.username)
    else:
        form = EducationForm(instance=edu_exp)

    context = {
        'form' : form,
        'edu_exp' : edu_exp,
        'title' : 'Edit Education',
        'template_data' : {'title': 'Edit Education'}
    }
    return render(request, 'profiles/education_form.html', context)

@login_required
def delete_education(request, exp_id):
    # Delete old Education
    # Get Associated Education
    edu_exp = get_object_or_404(Education, pk=exp_id, profile__user=request.user)

    if request.method == 'POST':
        edu_exp.delete()
        messages.success(request, 'Education Deleted!')
        return redirect('profiles.detail', username=request.user.username)
    
    context = {
        'edu_exp' : edu_exp,
        'template_data' : {'title' : 'Delete Education'}
    }
    return render(request, 'profiles/education_delete.html', context)