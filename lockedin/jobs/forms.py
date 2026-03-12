from django import forms
from .models import Job
from geopy.geocoders import Nominatim

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','start_date', 'end_date', 'description', 'skills', 
                  'salary_upper', 'salary_lower', 'location', 'classification', 'isSponsoring']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'E.g. Software Engineer, SDE'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows' : 6,
                'placeholder': 'Describe what the requirements/responsibilities are...'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class' : 'form-control',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class' : 'form-control',
                'type': 'datetime-local'
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Python, Django, Bootstrap, React, SQL, Git'
            }),
            'salary_upper': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maximum Salary'
            }),
            'salary_lower': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minimum Salary'
            }),
            'location' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Enter as a street address or city, state. Can also input N/A, etc.'
            }),
            'classification' : forms.Select(attrs={
                'class' : 'form-select'
            }),
            'isSponsoring' : forms.CheckboxInput(attrs={
                'class' : 'form-check-input',
            }),
        }
        labels = {
            'title' : 'Job Title',
            'start_date' : 'Start Date', 
            'end_date' : 'End Date', 
            'description' : 'Job Description', 
            'skills' : 'Skills', 
            'salary_upper' : 'Max. Salary', 
            'salary_lower' : 'Min. Salary', 
            'location' : 'Location',
            'classification' : 'Job Classfication', 
            'isSponsoring' : 'Visa Sponsoring'
        }
    
    # override default form save function to also calculate geocoordinates of the job location (if location given)
    def save(self, commit=True):
        job = super().save(commit=False)

        # use geopy to geocode the location
        location_text = self.cleaned_data.get('location')   # clean location text
        if (location_text and                               # if not holding null
                location_text.upper() != "N/A" and          # ignore a few "no location" signifiers
                location_text.upper() != "NA" and
                location_text.upper() != "NOT APPLICABLE" and
                location_text.upper() != "REMOTE" and
                location_text.upper() != "NO LOCATION"):
            
            geolocator = Nominatim(user_agent="lockedin_app")   # create geolocating client
            result = geolocator.geocode(location_text)          # geocode location text

            if result:  # if we get a valid response, overwrite coordinate fields
                job.latitude = result.latitude
                job.longitude = result.longitude

        if commit:
            job.save()

        return job

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['end_date'].required = False