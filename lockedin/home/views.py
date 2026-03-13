from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from jobs.models import Job
from profiles.models import Profile, Notification

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
                template_data['jobs'] = [] # Set all jobs to empty values as there is no need for jobs in the Recruiter's feed
                posted_jobs = Job.objects.filter(recruiter=request.user) # get all the jobs made by the recruiter
                template_data['posted_jobs'] = posted_jobs
                template_data['profiles'] = Profile.objects.all().filter(role='employee').exclude(user=request.user) # get all the employee profiles

                recommendation_skills = []
                for job in posted_jobs: # loop through all the jobs
                    for skill in job.get_skills_list():
                        skill = skill.strip().lower()
                        if skill:
                            if skill not in recommendation_skills: # and get all of the unique skills in Title Case into the job skill list
                                recommendation_skills.append(skill.title())

                template_data['skills'] = recommendation_skills
                notifications = Notification.objects.filter(user=request.user).order_by('-created')[:10]
                template_data['notifications'] = notifications

    return render(request, 'home/index.html', {
        'template_data': template_data})


def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request,
                  'home/about.html',
                  {'template_data': template_data})
