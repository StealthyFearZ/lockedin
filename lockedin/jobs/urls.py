from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="jobs.index"),
    path('<int:id>/', views.listing, name="jobs.listing"),
    path('<int:id>/apply/', views.apply , name="jobs.apply"),
    path('<int:id>/edit/', views.edit, name="jobs.edit"),
    path('<int:id>/post/', views.post, name="jobs.post"),
    path('applications/', views.applications, name="jobs.applications"),
    path('applications/<int:appId>/status/<str:targetStatus>/', views.edit_application_status, name="jobs.change_status"),
]