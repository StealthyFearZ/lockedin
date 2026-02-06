from django.urls import path
from . import views

urlpatterns = [
    path('edit/', views.profile_edit, name='profiles.edit'),
    path('<str:username>/', views.profile_view, name='profiles.detail'),
    path('', views.profile_view, name='profiles.my_profile'),
]