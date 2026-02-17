from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Application
from django.contrib.auth.decorators import login_required
from .forms import JobForm

# Create your views here.
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        jobs = (Job.objects.filter(title__icontains=search_term.strip()) | Job.objects.filter(skills__icontains=search_term.strip()) | Job.objects.filter(recruiter__username__icontains=search_term.strip())).distinct() #distinct needed to ensure that jobs can be found by name OR skills OR recruiter rather than only if both of them overlap
    else:
        jobs = Job.objects.all()

    location = request.GET.get('location','').strip()
    if location:
        jobs = jobs.filter(location__icontains=location)

    classification = request.GET.get('classification','').strip()
    if classification: # Slight error here, was using location, fixed it to classification
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
    job = get_object_or_404(Job, pk=id)
    template_data = {}
    template_data['title'] = job.title
    template_data['job'] = job
    template_data['company'] = job.recruiter
    return render(request, 'jobs/listings.html', {'template_data' : template_data})

@login_required
def edit(request, id):
    job = get_object_or_404(Job, pk=id)
    if job.recruiter != request.user: # only recruiter should be able to edit
        return redirect("jobs.listing", id=job.id)

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect("jobs.listing", id=job.id)
    else:
        form = JobForm(instance=job)

    template_data = {}
    template_data["title"] = "Edit Job"
    template_data["form"] = form
    template_data["job"] = job
    return render(request, "jobs/edit.html", {"template_data": template_data})

@login_required
def post(request):
    template_data = {}
    return render(request, 'jobs/post.html', {'template_data' : template_data})

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