from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about_me, name="about"),
    path("projects/", views.projects, name="projects"),
    path("resumes/", views.resumes, name="resumes"),
    path("links/", views.links, name="links"),
]