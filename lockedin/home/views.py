from django.shortcuts import render
from jobs.models import Job

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'LockedIn'
    template_data['jobs'] = Job.objects.all()
    return render(request, 'home/index.html', {
        'template_data': template_data})

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request,
                  'home/about.html',
                  {'template_data': template_data})
