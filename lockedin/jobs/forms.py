from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','start_date', 'end_date', 'description', 'skills', 
                  'salary_upper', 'salary_lower', 'location', 'location_x', 'location_y', 'classification', 'isSponsoring']
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
                'placeholder': 'Python, Django, Bootstrap, React, SQL, Git (comma seperated)'
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
                'placeholder' : 'e.g. New York, Atlanta'
            }),
            'location_x' : forms.NumberInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'X-Coordinates'
            }),
            'location_y' : forms.NumberInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Y-Coordinates'
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
            'location_x' : 'Location X-Coords',
            'location_y' : 'Location Y-Coords',
            'classification' : 'Job Classfication', 
            'isSponsoring' : 'Visa Sponsoring'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['end_date'].required = False