from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    headline    = models.CharField(max_length = 150)
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    about       = models.TextField(blank=True)
    skills      = models.TextField()
    profile_pic = models.ImageField(null=True, upload_to='profile_pictures/', blank=True)

    