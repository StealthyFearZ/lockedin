from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from jobs.models import Job
from profiles.models import Profile

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'LockedIn'
    template_data['jobs'] = Job.objects.all()
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.all().filter(user=request.user).first()
        template_data['profile'] = profile
        template_data['skills'] = profile.get_skills_list

    return render(request, 'home/index.html', {
        'template_data': template_data})


def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request,
                  'home/about.html',
                  {'template_data': template_data})
