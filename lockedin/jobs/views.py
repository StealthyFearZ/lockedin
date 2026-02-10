from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        jobs = Job.objects.filter(title__icontains=search_term)
    else:
        jobs = Job.objects.all()
    template_data = {}
    template_data['title'] = 'Job Listings'
    template_data['jobs'] = jobs
    return render(request, 'jobs/index.html',
                  {'template_data': template_data})

def listing(request, id):
    job = Job.objects.get(id=id)
    template_data = {}
    template_data['title'] = job.title
    template_data['start_date'] = job.start_date
    template_data['end_date'] = job.end_date
    template_data['description'] = job.description
    template_data['company'] = job.recruiter
    template_data['skills'] = job.skills
    template_data['skills'] = job.skills   
    template_data['salary_top'] = job.salary_upper
    template_data['salary_bottom'] = job.salary_lower
    template_data['location'] = job.location
    template_data['classification'] = job.classification
    template_data['sponsoring'] = job.isSponsoring
    return render(request, 'jobs/listings.html', {'template_data' : template_data})

@login_required
def edit(request, id):
    return None

@login_required
def post(request):
    return None