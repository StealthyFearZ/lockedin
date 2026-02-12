from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Job(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add="true")
    title = models.CharField(help_text="What is the job title?", max_length = 255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank="true", null="true")
    description = models.TextField()
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    skills = models.CharField(help_text="List all of your skills(E.g: Project Management, Agile Methodologies, etc.)", max_length = 255)
    salary_upper = models.IntegerField()
    salary_lower = models.IntegerField()
    location = models.CharField(help_text="Where is this job listing located? Where do employees work from?", max_length = 255)
    classification = models.CharField(help_text="E.g: On-Site, Hybrid, Remote", max_length = 255)
    isSponsoring = models.BooleanField(help_text="True: for OPT/CPT, F-1, J-1, etc., False: US citizens/Green Card holders")

    def __str__(self):
        return str(self.recruiter) + " - " + str(self.title)

    def get_skills_list(self):
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]

