from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='my_profile'),
    path('edit/', views.profile_edit, name='profile_edit'),
    path('<str:username>/', views.profile_view, name='profile_detail'),
]