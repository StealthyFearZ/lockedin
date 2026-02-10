from django.urls import path
from . import views

urlpatterns = [
    # Profile URLs
    path('edit/', views.profile_edit, name='profiles.edit'),
    path('', views.profile_view, name='profiles.my_profile'),

    # Experience URLs
    path('work-experience/add/', views.add_experience, name='profiles.add_experience'),
    path('work-experience/<int:exp_id>/edit/', views.edit_experience, name='profiles.edit_experience'),
    path('work-experience/<int:exp_id>/delete/', views.delete_experience, name='profiles.delete_experience'),

    path('<str:username>/', views.profile_view, name='profiles.detail'),
]