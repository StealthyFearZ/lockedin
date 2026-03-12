from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Application
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.contrib import messages
from django.http import JsonResponse
from .forms import JobForm
from profiles.models import Profile

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
    if classification:
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
    template_data['job'] = job
    template_data['start_date'] = job.start_date
    template_data['end_date'] = job.end_date
    template_data['description'] = job.description
    template_data['company'] = job.recruiter
    template_data['skills'] = job.skills
    template_data['salary_top'] = job.salary_upper
    template_data['salary_bottom'] = job.salary_lower
    template_data['location'] = job.location
    template_data['classification'] = job.classification
    template_data['sponsoring'] = job.isSponsoring
    template_data['job'] = job
    return render(request, 'jobs/listings.html', {'template_data' : template_data})

@login_required
def edit(request, id):
    # Edit the job using same template as post basically
    job = get_object_or_404(Job, id=id, recruiter=request.user)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('jobs.listing', id=job.id)
    else:
        form = JobForm(instance=job)
    
    context = {
        'template_data': {
            'title': f'Edit Job: {job.title}',
            'form': form,
            'job': job
        }
    }
    return render(request, 'jobs/edit.html', context)

@login_required
def post(request):
    # Post the job and make sure it saves the recruiter
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('jobs.recruiter_dashboard')
    else:
        form = JobForm()
    
    context = {
        'template_data': {
            'title': 'Post a Job',
            'form': form
        }
    }
    return render(request, 'jobs/post.html', context)

def map(request):
    jobs = Job.objects.all()
    template_data = {}
    template_data['title'] = 'Job Map'
    template_data['jobs'] = jobs
    return render(request, 'jobs/map.html', {"jobs_json": serialize("json", jobs), 
                                             'template_data': template_data})
@login_required
def apply(request, id):
    job = get_object_or_404(Job, id=id)

    # cannot apply to same job more than once
    if Application.objects.filter(user=request.user, job=job).exists():
        return redirect('jobs.listing', id=id)
    
    if request.method == 'POST':
        if not Application.objects.filter(user=request.user, job=job).exists():
            note = request.POST.get('note', '')
            Application.objects.create(user=request.user, job=job, note=note)
        return redirect('jobs.applications')
    template_data = {}
    template_data["job"] = job
    return render(request, 'jobs/apply.html', {'template_data' : template_data})

@login_required
def applications(request):
    applications = Application.objects.filter(user=request.user)

    status = request.GET.get('status','').strip()
    if len(status) > 0:
        applications = applications.filter(status=status)

    template_data = {}
    template_data["apps"] = applications
    template_data["status_choices"] = Application.ApplicationChoices.choices
    return render(request, 'jobs/applications.html',
                  {'template_data': template_data})

@login_required
def edit_application_status(request, appId, targetStatus):
    # Ensure the user owns the application before editing
    app = get_object_or_404(Application, id=appId, user=request.user)
    app.status = targetStatus
    app.save()
    return redirect('jobs.applications')

def map(request):
    jobs = Job.objects.all()
    template_data = {}
    template_data['title'] = 'Job Map'
    template_data['jobs'] = jobs
    return render(request, 'jobs/map.html', {"jobs_json": serialize("json", jobs), 
                                             'template_data': template_data})

# Kanban Stuff

@login_required
def recruiter_dashboard(request):
    # Only show jobs posted by the current user (recruiter)
    jobs = Job.objects.filter(recruiter=request.user).order_by('-created_at')
    
    context = {
        'jobs': jobs,
        'template_data': {'title': 'Recruiter Dashboard'}
    }
    return render(request, 'jobs/recruiter_dashboard.html', context)

@login_required
def application_pipeline(request, job_id):
    #get job
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    
    # find applications
    applications = Application.objects.filter(job=job).select_related('user', 'user__profile')
    
    # order applications into status of application for kanban board
    pipeline = {
        'applied': applications.filter(status=Application.ApplicationChoices.APPLIED),
        'review': applications.filter(status=Application.ApplicationChoices.REVIEW),
        'interview': applications.filter(status=Application.ApplicationChoices.INTERVIEW),
        'offer': applications.filter(status=Application.ApplicationChoices.OFFER),
        'closed': applications.filter(status=Application.ApplicationChoices.CLOSED),
    }
    
    context = {
        'job': job,
        'pipeline': pipeline,
        'template_data': {'title': f'Applications - {job.title}'}
    }
    return render(request, 'jobs/application_pipeline.html', context)

@login_required
def update_application_status(request, application_id):
    # Get application
    if request.method == 'POST':
        application = get_object_or_404(Application, id=application_id, job__recruiter=request.user)
        new_status = request.POST.get('status')
        
        # Validate new status
        valid_statuses = [choice[0] for choice in Application.ApplicationChoices.choices]
        if new_status in valid_statuses:
            application.status = new_status
            application.save()
            messages.success(request, f'Application status updated to {application.get_status_display()}')
        else:
            messages.error(request, 'Invalid status')
    
    return redirect('jobs.application_pipeline', job_id=application.job.id)

@login_required
def update_application_note(request, application_id):
    # add note to applicant
    if request.method == 'POST':
        application = get_object_or_404(Application, id=application_id, job__recruiter=request.user)
        note = request.POST.get('note', '')
        application.note = note[:150] # Can only be 150 chars
        application.save()
        messages.success(request, 'Note updated successfully')
    
    return redirect('jobs.application_pipeline', job_id=application.job.id)
