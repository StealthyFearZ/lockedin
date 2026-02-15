from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="jobs.index"),
    path('<int:id>/', views.listing, name="jobs.listing"),
    path('<int:id>/edit/', views.edit, name="jobs.edit"),
    path('<int:id>/post/', views.post, name="jobs.post"),
    path('map', views.map, name="jobs.map"),
]