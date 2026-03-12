from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="jobs.index"),
    path('<int:id>/', views.listing, name="jobs.listing"),
    path('<int:id>/apply/', views.apply , name="jobs.apply"),
    path('<int:id>/edit/', views.edit, name="jobs.edit"),
    path('post/', views.post, name="jobs.post"),
    path('applications/', views.applications, name="jobs.applications"),
    path('applications/<int:appId>/status/<str:targetStatus>/', views.edit_application_status, name="jobs.change_status"),
    path('map', views.map, name="jobs.map"),
    # Kanban stuff
    path('recruiter/dashboard/', views.recruiter_dashboard, name='jobs.recruiter_dashboard'),
    path('recruiter/job/<int:job_id>/map/', views.application_map, name='jobs.application_map'),
    path('recruiter/job/<int:job_id>/pipeline/', views.application_pipeline, name='jobs.application_pipeline'),
    path('recruiter/application/<int:application_id>/update-status/', views.update_application_status, name='jobs.update_application_status'),
    path('recruiter/application/<int:application_id>/update-note/', views.update_application_note, name='jobs.update_application_note'),
]