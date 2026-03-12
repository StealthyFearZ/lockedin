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
    template_data['profiles'] = []
    template_data['posted_jobs'] = [] #Jobs posted by a recruiter profile


    if request.user.is_authenticated:
        profile = Profile.objects.all().filter(user=request.user).first()
        template_data['profile'] = profile
        if profile:
            if profile.role == 'employee':
                template_data['skills'] = profile.get_skills_list() #maintain code for employee as default role
            elif profile.role == 'recruiter':
                template_data['jobs'] = [] # Need to change this eventually, need to include both jobs and recruiters
                posted_jobs = Job.objects.filter(recruiter=request.user) # gets all jobs related to this Recruiter
                template_data['posted_jobs'] = posted_jobs
                recommendation_skills = []
                for job in posted_jobs:
                    for skill in job.get_skills_list():
                        skill = skill.strip().lower() #ensure overall equality check
                        if skill: # check that the skill exists as a word
                            if skill not in recommendation_skills: # check that the skill does not already exist in the list
                                recommendation_skills.append(skill.title()) # Add skill into the list in Title Case("hello world" -> "Hello World")
                template_data['skills'] = recommendation_skills
                template_data['profiles'] = Profile.objects.filter(role='employee').exclude(user=request.user) # get all employee profiles save for the current user

    return render(request, 'home/index.html', {
        'template_data': template_data})


def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request,
                  'home/about.html',
                  {'template_data': template_data})
