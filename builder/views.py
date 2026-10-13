from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (
    ContactForm,
    ProfileForm,
    ProjectForm,
    ResumeForm,
    LinkForm,
    FormBuilderForm,
)
from .models import Profile, Project, Resume, Link, Form, FormSubmission
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)

    return render(request, "dashboard.html", {"profile": profile})


@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
            user=request.user,
        )

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = ProfileForm(
            instance=profile,
            user=request.user,
        )

    featured_objects = {
        "projects": [
            {"id": obj.id, "label": obj.title}
            for obj in Project.objects.filter(user=request.user)
        ],
        "resumes": [
            {"id": obj.id, "label": obj.display_name}
            for obj in Resume.objects.filter(user=request.user)
        ],
        "links": [
            {"id": obj.id, "label": obj.display_name}
            for obj in Link.objects.filter(user=request.user)
        ],
        "forms": [
            {"id": obj.id, "label": obj.form_name}
            for obj in Form.objects.filter(user=request.user)
        ],
    }

    return render(
        request,
        "edit_profile.html",
        {
            "form": form,
            "featured_objects": featured_objects,
        },
    )


@login_required
def manage_projects(request):
    projects = Project.objects.filter(user=request.user)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect("manage_projects")

    else:
        form = ProjectForm()

    return render(
        request,
        "manage_projects.html",
        {
            "projects": projects,
            "form": form,
        },
    )


@login_required
def edit_project(request, project_id):
    project = Project.objects.get(id=project_id, user=request.user)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)

        if form.is_valid():
            form.save()
            return redirect("manage_projects")

    else:
        form = ProjectForm(instance=project)

    return render(request, "edit_project.html", {"form": form})


@login_required
def delete_project(request, project_id):
    project = Project.objects.get(id=project_id, user=request.user)

    if request.method == "POST":
        project.delete()
        return redirect("manage_projects")

    return render(request, "delete_project.html", {"project": project})


@login_required
def manage_resumes(request):
    resumes = Resume.objects.filter(user=request.user)

    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect("manage_resumes")

    else:
        form = ResumeForm()

    return render(
        request,
        "manage_resumes.html",
        {
            "resumes": resumes,
            "form": form,
        },
    )


@login_required
def delete_resume(request, resume_id):
    resume = Resume.objects.get(id=resume_id, user=request.user)

    if request.method == "POST":
        resume.delete()
        return redirect("manage_resumes")

    return render(request, "delete_resume.html", {"resume": resume})


@login_required
def manage_links(request):
    links = Link.objects.filter(user=request.user)

    if request.method == "POST":
        form = LinkForm(request.POST, request.FILES)

        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()
            return redirect("manage_links")

    else:
        form = LinkForm()

    return render(
        request,
        "manage_links.html",
        {
            "links": links,
            "form": form,
        },
    )


@login_required
def delete_link(request, link_id):
    link = Link.objects.get(id=link_id, user=request.user)

    if request.method == "POST":
        link.delete()
        return redirect("manage_links")

    return render(request, "delete_link.html", {"link": link})


@login_required
def manage_forms(request):
    forms = Form.objects.filter(user=request.user)

    if request.method == "POST":
        form = FormBuilderForm(request.POST)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return redirect("manage_forms")

    else:
        form = FormBuilderForm()

    return render(
        request,
        "manage_forms.html",
        {
            "forms": forms,
            "form": form,
        },
    )


@login_required
def edit_form(request, form_id):
    form_item = Form.objects.get(id=form_id, user=request.user)

    if request.method == "POST":
        form = FormBuilderForm(request.POST, instance=form_item)

        if form.is_valid():
            form.save()
            return redirect("manage_forms")

    else:
        form = FormBuilderForm(instance=form_item)

    return render(request, "edit_form.html", {"form": form})


@login_required
def delete_form(request, form_id):
    form_item = Form.objects.get(id=form_id, user=request.user)

    if request.method == "POST":
        form_item.delete()
        return redirect("manage_forms")

    return render(request, "delete_form.html", {"form_item": form_item})


@login_required
def form_submissions(request, form_id):
    form_item = Form.objects.get(id=form_id, user=request.user)

    submissions = FormSubmission.objects.filter(form=form_item)

    return render(
        request,
        "form_submissions.html",
        {
            "form_item": form_item,
            "submissions": submissions,
        },
    )


def home(request, username):
    profile = Profile.objects.get(user__username=username)

    featured_object = None
    featured_form = None
    contact_form = None

    if profile.featured_section == "about":
        featured_object = profile

    elif profile.featured_section and profile.featured_object_id:
        if profile.featured_section == "projects":
            featured_object = Project.objects.filter(
                id=profile.featured_object_id,
                user=profile.user,
            ).first()

        elif profile.featured_section == "resumes":
            featured_object = Resume.objects.filter(
                id=profile.featured_object_id,
                user=profile.user,
            ).first()

        elif profile.featured_section == "links":
            featured_object = Link.objects.filter(
                id=profile.featured_object_id,
                user=profile.user,
            ).first()

        elif profile.featured_section == "forms":
            featured_object = Form.objects.filter(
                id=profile.featured_object_id,
                user=profile.user,
            ).first()

    if profile.featured_section == "forms" and featured_object:
        featured_form = featured_object

        contact_form = ContactForm(
            textbox_prompt=featured_form.textbox_prompt,
            checkbox_prompt=featured_form.checkbox_prompt,
            include_name=featured_form.include_name,
            name_required=featured_form.name_required,
            include_email=featured_form.include_email,
            email_required=featured_form.email_required,
        )

    social_links = Link.objects.filter(
        user=profile.user,
        is_social=True,
    )

    context = {
        "profile": profile,
        "is_homepage": True,
        "featured_object": featured_object,
        "social_links": social_links,
        "featured_form": featured_form,
        "contact_form": contact_form,
    }

    return render(request, "index.html", context=context)


def about_me(request, username):
    profile = Profile.objects.get(user__username=username)

    context = {
        "profile": profile,
    }

    return render(request, "about_me.html", context=context)


def projects(request, username):
    projects = Project.objects.filter(user__username=username)
    profile = Profile.objects.get(user__username=username)

    context = {
        "projects": projects,
        "profile": profile,
    }

    return render(request, "projects.html", context=context)


def resumes(request, username):
    resumes = Resume.objects.filter(user__username=username)
    profile = Profile.objects.get(user__username=username)

    context = {
        "resumes": resumes,
        "profile": profile,
    }

    return render(request, "resumes.html", context=context)


def links(request, username):
    links = Link.objects.filter(user__username=username)
    profile = Profile.objects.get(user__username=username)

    context = {
        "links": links,
        "profile": profile,
    }

    return render(request, "links.html", context=context)


def forms(request, username):
    forms = Form.objects.filter(user__username=username)
    profile = Profile.objects.get(user__username=username)
    form_pairs = [
        (
            form,
            ContactForm(
                textbox_prompt=form.textbox_prompt,
                checkbox_prompt=form.checkbox_prompt,
                include_name=form.include_name,
                name_required=form.name_required,
                include_email=form.include_email,
                email_required=form.email_required,
            ),
        )
        for form in forms
    ]

    context = {
        "form_pairs": form_pairs,
        "profile": profile,
    }

    return render(request, "forms.html", context=context)


def form_submit(request, username):
    redirect_view = "home" if request.POST.get("return_to") == "home" else "forms"

    if request.method != "POST":
        messages.error(request, "Invalid request.")
        return redirect(redirect_view, username=username)

    form_id = request.POST.get("form_id")
    if not form_id:
        messages.error(request, "We couldn't identify the form you submitted.")
        return redirect(redirect_view, username=username)
    try:
        form = Form.objects.get(
            id=form_id,
            user__username=username,
        )
    except Form.DoesNotExist:
        messages.error(request, "That form is no longer available.")
        return redirect(redirect_view, username=username)

    contact_form = ContactForm(
        request.POST,
        textbox_prompt=form.textbox_prompt,
        checkbox_prompt=form.checkbox_prompt,
        include_name=form.include_name,
        name_required=form.name_required,
        include_email=form.include_email,
        email_required=form.email_required,
    )

    if not contact_form.is_valid():
        messages.error(request, "Please correct the errors in the form.")
        return redirect(redirect_view, username=username)

    submission = FormSubmission(
        form=form,
        visitor_name=contact_form.cleaned_data.get("visitor_name"),
        visitor_email=contact_form.cleaned_data.get("visitor_email"),
        textbox=contact_form.cleaned_data.get("textbox"),
        checkbox=contact_form.cleaned_data.get("checkbox"),
    )

    submission.save()
    messages.success(request, "Submission success!")

    return redirect(redirect_view, username=username)
