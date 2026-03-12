from django.contrib import admin
from .models import Profile
from jobs.admin import export_as_csv

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    actions = [export_as_csv]