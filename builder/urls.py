from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/profile/", views.edit_profile, name="edit_profile"),
    path("dashboard/projects/", views.manage_projects, name="manage_projects"),
    path("dashboard/projects/<int:project_id>/edit/", views.edit_project, name="edit_project"),
    path(
        "dashboard/projects/<int:project_id>/delete/",
        views.delete_project,
        name="delete_project",
    ),
    path("dashboard/resumes/", views.manage_resumes, name="manage_resumes"),
    path(
        "dashboard/resumes/<int:resume_id>/delete/",
        views.delete_resume,
        name="delete_resume",
    ),
    path("dashboard/links/", views.manage_links, name="manage_links"),
    path(
        "dashboard/links/<int:link_id>/delete/",
        views.delete_link,
        name="delete_link",
    ),
    path("dashboard/forms/", views.manage_forms, name="manage_forms"),
    path(
        "dashboard/forms/<int:form_id>/edit/",
        views.edit_form,
        name="edit_form",
    ),
    path(
        "dashboard/forms/<int:form_id>/delete/",
        views.delete_form,
        name="delete_form",
    ),
    path(
        "dashboard/forms/<int:form_id>/submissions/",
        views.form_submissions,
        name="form_submissions",
    ),

    
    path("<str:username>/", views.home, name="home"),
    path("<str:username>/about/", views.about_me, name="about"),
    path("<str:username>/projects/", views.projects, name="projects"),
    path("<str:username>/resumes/", views.resumes, name="resumes"),
    path("<str:username>/links/", views.links, name="links"),
    path("<str:username>/forms/", views.forms, name="forms"),
    path("<str:username>/forms/submit/", views.form_submit, name="form_submit"),
    
]