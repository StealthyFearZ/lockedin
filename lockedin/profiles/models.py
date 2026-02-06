from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator

# Create your models here.
class Profile(models.Model):
    # Model Information
    headline     = models.CharField(max_length = 150, help_text="Example: CS @ GT")
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    about        = models.TextField(blank=True, help_text="Tells us about yourself")
    skills       = models.TextField(help_text="Add your skills")
    profile_pic  = models.ImageField(null=True, upload_to='profile_pictures/', blank=True)
    # URL Links
    github_url   = models.URLField(blank=True, validators=[URLValidator()])
    linkedin_url = models.URLField(blank=True, validators=[URLValidator()])
    portfolio_url = models.URLField(blank=True, validators=[URLValidator()])
    # Times
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_skills_list(self):
        # Return a List of Skills
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]
    
    class Meta:
        ordering = ['-time_created']


    