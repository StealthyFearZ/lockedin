from django.contrib import admin
from .models import Profile, Notification, ProfileSearch
from jobs.admin import export_as_csv

# Register your models here.
@admin.register(Profile)
@admin.register(Notification)
@admin.register(ProfileSearch)
class ProfileAdmin(admin.ModelAdmin):
    actions = [export_as_csv]