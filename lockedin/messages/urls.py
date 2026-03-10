from django.urls import path
from . import views

urlpatterns = [
    # Profile URLs
    path('', views.messages_list, name='messages.list'),
]