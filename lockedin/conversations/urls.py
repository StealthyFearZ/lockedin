from django.urls import path
from . import views

urlpatterns = [
    # Profile URLs
    path('', views.conversations_list, name='conversations.list'),
]