from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import JsonResponse

# Create your views here.
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        jobs = (Job.objects.filter(title__icontains=search_term) | Job.objects.filter(skills__icontains=search_term)).distinct() #distinct needed to ensure that jobs can be found by name OR skills rather than only if both of them overlap
    else:
        jobs = Job.objects.all()

    location = request.GET.get('location','').strip()
    if location:
        jobs = jobs.filter(location__icontains=location)

    classification = request.GET.get('classification','').strip()
    if location:
        jobs = jobs.filter(classification__icontains=classification)

    min_salary = request.GET.get('min_salary','').strip()
    try:
        min_salary_int = int(min_salary)
        jobs = jobs.filter(salary_upper__gte=min_salary_int) #gte = Upper Salary bound greater than or equal to Minimum Salary. Filters all jobs that have salaries greater than the minimum bound.
    except ValueError:
        pass

    max_salary = request.GET.get('max_salary','').strip()
    try:
        max_salary_int = int(max_salary)
        jobs = jobs.filter(salary_lower__lte=max_salary_int) #lte = Lower Salary bound lesser than or equal to Maximum Salary. Filters all jobs that have lower salaries lesser than the maxmimum bound. Both values ensure the Jobs displayed fall within the filter bounds
    except ValueError:
        pass

    sponsorship = request.GET.get('sponsorship','').strip()
    if sponsorship == "Sponsoring":
        jobs = jobs.filter(isSponsoring=True)
    elif sponsorship == "Not Sponsoring":
        jobs = jobs.filter(isSponsoring=False)

    skills_input = request.GET.get('skills','').strip()
    if skills_input:
        skills_list = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
        for skill in skills_list:
            jobs = jobs.filter(skills__icontains=skill)

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

def map(request):
    jobs = Job.objects.all()
    template_data = {}
    template_data['title'] = 'Job Map'
    template_data['jobs'] = jobs
    return render(request, 'jobs/map.html', {"jobs_json": serialize("json", jobs), 
                                             'template_data': template_data})