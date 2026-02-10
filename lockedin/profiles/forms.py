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
        fields = ['job', 'company', 'location', 'start_data',
                 'end_data', 'current_job', 'description']
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