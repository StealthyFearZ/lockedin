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
    is_private   = models.BooleanField(default=False)
    # URL Links
    github_url   = models.URLField(blank=True, validators=[URLValidator()])
    linkedin_url = models.URLField(blank=True, validators=[URLValidator()])
    portfolio_url = models.URLField(blank=True, validators=[URLValidator()])
    # Times
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    # Functions
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_skills_list(self):
        # Return a List of Skills
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]
    
    class Meta:
        ordering = ['-time_created']

class Experience(models.Model):
    # Model Information
    profile     = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    start_date  = models.DateField()
    end_date    = models.DateField(blank = True, null=True)
    job         = models.CharField(max_length=150)
    location    = models.CharField(max_length=150)
    description = models.TextField()
    current_job = models.BooleanField(default=False)
    company     = models.CharField(max_length=150)
    # Times
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    # Functions
    def __str__(self):
        return f"{self.job} @ {self.company}"
    
    class Meta:
        ordering = ['-start_date']

class Education(models.Model):
    # Education Info
    # List of degrees you can select from
    degrees = [
        ('high_school', 'High School'),
        ('associate', 'Associate Degree'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'Ph.D.'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='educations')
    start_date = models.DateField()
    end_date = models.DateField(blank = True, null = True)
    school_name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    current_school = models.BooleanField(default=False)
    degree = models.CharField(max_length=50, choices=degrees)
    field_of_study = models.CharField(max_length=200, blank=True)
    # Times
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    #Functions
    def __str__(self):
        return f"{self.profile.user.username} @ {self.school_name}"
    
    class Meta:
        ordering = ['-start_date']