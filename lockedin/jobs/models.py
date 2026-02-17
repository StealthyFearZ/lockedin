from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Job(models.Model):
    classificationChoices = [
        ("On-Site", "on-site"),
        ("Hybrid", "hybrid"),
        ("Remote", "remote"),
    ]
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add="true")
    title = models.CharField(help_text="What is the job title?", max_length = 255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank="true", null="true")
    description = models.TextField()
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    skills = models.TextField(help_text="List all of your skills(E.g: Project Management, Agile Methodologies, etc.)")
    salary_upper = models.IntegerField()
    salary_lower = models.IntegerField()
    location = models.CharField(help_text="Where is this job listing located? Where do employees work from?", max_length = 255)
    classification = models.CharField(choices=classificationChoices, max_length=20)
    isSponsoring = models.BooleanField(help_text="True: for OPT/CPT, F-1, J-1, etc., False: US citizens/Green Card holders")

    def __str__(self):
        return str(self.recruiter) + " - " + str(self.title)

    def get_skills_list(self):
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]

# intermediary model
class Application(models.Model):
    # type enum (hardcoded application type)
    class ApplicationChoices(models.TextChoices):
        APPLIED = "AP", "Applied"
        REVIEW = "RE", "Review"
        INTERVIEW = "IN", "Interview"
        OFFER = "OF", "Offer"
        CLOSED = "CL", "Closed"
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add="true")
    choices = models.TextChoices('Applied', 'Review', 'Interview', 'Offer', 'Closed')
    status = models.CharField(
        max_length = 2,
        choices=ApplicationChoices,
        default=ApplicationChoices.APPLIED)
    
    # restricting so only one application per job per user
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'job'],
                name="single_application_per_user",
                violation_error_message="User has already applied to this job."
            )
        ]
