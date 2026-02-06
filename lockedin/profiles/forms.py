from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    # Creates and Updates Profiles

    class Meta:
        model = Profile
        fields = ['headline', 'about', 'skills', 'profile_pic', 
                  'linkedin_url', 'github_url', 'portfolio_url']