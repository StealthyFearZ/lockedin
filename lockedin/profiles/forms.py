from django import forms
from .models import Profile, Experience

class ProfileForm(forms.ModelForm):
    # Creates and Updates Profiles

    class Meta:
        model = Profile
        fields = ['headline', 'about', 'skills', 'profile_pic', 
                  'linkedin_url', 'github_url', 'portfolio_url']
        widgets = {
            'headline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'example: Student at Georgia Tech'
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell others about yourself'
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Python, Django, Bootstrap, React, SQL, Git (comma seperated)'
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/yourprofile'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/yourusername'
            }),
            'portfolio_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourportfolio.com'
            }),
        }
        labels = {
            'headline': 'Professional Headline',
            'about': 'About Me',
            'skills': 'Skills',
            'profile_picture': 'Profile Picture',
            'linkedin_url': 'LinkedIn URL',
            'github_url': 'GitHub URL',
            'portfolio_url': 'Portfolio Website',
        }

class ExperienceForm(forms.ModelForm):
    # CRUD for Experiences

    class Meta:
        model = Experience
        fields = ['job', 'company', 'location', 'start_date',
                 'end_date', 'current_job', 'description']
        widgets = {
            'job' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Ex: VLSI Engineer'
            }),
            'company' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Ex: NVIDIA'
            }),
            'location' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Ex: Santa Clara, CA'
            }),
            'start_date' : forms.DateInput(attrs={
                'class' : 'form-control',
                'type' : 'date'
            }),
            'end_date' : forms.DateInput(attrs={
                'class' : 'form-control',
                'type' : 'date'
            }),
            'current_job' : forms.CheckboxInput(attrs={
                'class' : 'form-check-input'
            }),
            'description' : forms.Textarea(attrs={
                'class' : 'form-control',
                'rows' : 4,
                'placeholder' : 'Describe your experience'
            }),
        }
    
    # Add Method to clean work Experience
    def clean(self):
        clean_data = super().clean
        current_job = clean_data.get('current_job')
        start_date  = clean_data.get('start_date')
        end_date    = clean_data.get('end_date')

        # If working a current job, then there should be no end date
        if current_job:
            clean_data['end_date'] = None
        elif not end_date:
            raise forms.ValidationError(
                'Must provide an end date, or check "Currently Working Here'
            )
        
        # Start Date must be before End Date
        if end_date and start_date and start_date > end_date:
            raise forms.ValidationError(
                "Start Date must be before End Date"
            )
        
        return clean_data