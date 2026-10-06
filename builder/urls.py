from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    
    path("<str:username>/", views.home, name="home"),
    path("<str:username>/about/", views.about_me, name="about"),
    path("<str:username>/projects/", views.projects, name="projects"),
    path("<str:username>/resumes/", views.resumes, name="resumes"),
    path("<str:username>/links/", views.links, name="links"),
    path("<str:username>/forms/", views.forms, name="forms"),
    path("<str:username>/forms/submit/", views.form_submit, name="form_submit"),
    
]