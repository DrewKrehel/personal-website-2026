from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (
    ContactForm,
    ProfileForm,
    ProjectForm,
    ResumeForm,
    LinkForm,
    FormBuilderForm,
    IndexThumbnailForm,
)
from .models import Profile, Project, Resume, Link, Form, FormSubmission
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        thumbnail_form = IndexThumbnailForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if thumbnail_form.is_valid():
            thumbnail_form.save()
            messages.success(
                request,
                "Index thumbnail updated successfully.",
            )
            return redirect("dashboard")
    else:
        thumbnail_form = IndexThumbnailForm(instance=profile)

    return render(
        request,
        "dashboard.html",
        {
            "profile": profile,
            "thumbnail_form": thumbnail_form,
        },
    )


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
    projects = Project.objects.filter(user=request.user).order_by("sort_order", "id")

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.sort_order = Project.objects.filter(user=request.user).count()
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

def _move_user_item(request, model, item_id, direction, redirect_name):
    """Move one of the user's items up or down in its list."""

    if direction not in ("up", "down"):
        return redirect(redirect_name)

    items = list(model.objects.filter(user=request.user).order_by("sort_order", "id"))

    # Find the item in this user's list.
    current_index = next(
        (index for index, item in enumerate(items) if item.id == item_id),
        None,
    )

    # Do nothing if the item doesn't belong to this user.
    if current_index is None:
        return redirect(redirect_name)

    # Calculate the position of the neighboring item.
    if direction == "up":
        neighbor_index = current_index - 1
    else:
        neighbor_index = current_index + 1

    # Do nothing if the item is already at the relevant boundary.
    if neighbor_index < 0 or neighbor_index >= len(items):
        return redirect(redirect_name)

    # Swap the two items.
    items[current_index], items[neighbor_index] = (
        items[neighbor_index],
        items[current_index],
    )

    # Save a clean sequence of positions: 0, 1, 2, 3, ...
    for position, item in enumerate(items):
        if item.sort_order != position:
            item.sort_order = position
            item.save(update_fields=["sort_order"])

    return redirect(redirect_name)


@login_required
@require_POST
def move_project(request, project_id, direction):
    return _move_user_item(request, Project, project_id, direction, "manage_projects")


@login_required
@require_POST
def move_resume(request, resume_id, direction):
    return _move_user_item(request, Resume, resume_id, direction, "manage_resumes")


@login_required
@require_POST
def move_link(request, link_id, direction):
    return _move_user_item(request, Link, link_id, direction, "manage_links")


@login_required
@require_POST
def move_form(request, form_id, direction):
    return _move_user_item(request, Form, form_id, direction, "manage_forms")


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
    resumes = Resume.objects.filter(user=request.user).order_by("sort_order", "id")

    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.sort_order = Resume.objects.filter(user=request.user).count()
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
    links = Link.objects.filter(user=request.user).order_by("sort_order", "id")

    if request.method == "POST":
        form = LinkForm(request.POST, request.FILES)

        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.sort_order = Link.objects.filter(user=request.user).count()
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
    forms = Form.objects.filter(user=request.user).order_by("sort_order", "id")

    if request.method == "POST":
        form = FormBuilderForm(request.POST)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.sort_order = Form.objects.filter(user=request.user).count()
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
def delete_submission(request, submission_id):
    submission = FormSubmission.objects.get(
        id=submission_id,
        form__user=request.user,
    )

    if request.method == "POST":
        form_id = submission.form.id
        submission.delete()
        messages.success(request, "Submission deleted successfully.")
        return redirect("form_submissions", form_id=form_id)

    return render(
        request,
        "delete_submission.html",
        {"submission": submission},
    )

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
    ).order_by("sort_order", "id")

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
    profile = Profile.objects.get(user__username=username)
    projects = Project.objects.filter(user=profile.user).order_by("sort_order", "id")

    context = {
        "projects": projects,
        "profile": profile,
    }

    return render(request, "projects.html", context=context)


def resumes(request, username):
    resumes = Resume.objects.filter(user__username=username).order_by(
        "sort_order", "id"
    )
    profile = Profile.objects.get(user__username=username)

    context = {
        "resumes": resumes,
        "profile": profile,
    }

    return render(request, "resumes.html", context=context)


def links(request, username):
    links = Link.objects.filter(user__username=username).order_by("sort_order", "id")
    profile = Profile.objects.get(user__username=username)

    context = {
        "links": links,
        "profile": profile,
    }

    return render(request, "links.html", context=context)


def forms(request, username):
    forms = Form.objects.filter(user__username=username).order_by("sort_order", "id")
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

    # Save the submission temporarily so a failed email cannot lose it.
    submission = FormSubmission(
        form=form,
        visitor_name=contact_form.cleaned_data.get("visitor_name"),
        visitor_email=contact_form.cleaned_data.get("visitor_email"),
        textbox=contact_form.cleaned_data.get("textbox"),
        checkbox=contact_form.cleaned_data.get("checkbox"),
    )
    submission.save()

    email_sent = False

    if form.email_submissions:
        if not form.user.email:
            messages.error(
                request,
                "The form owner's account has no email address. "
                "The submission was saved so it won't be lost.",
            )
        else:
            # Build the email from the submitted answers.
            email_lines = [
                f"Form: {form.form_name}",
                "",
            ]

            if submission.visitor_name:
                email_lines.append(f"Name: {submission.visitor_name}")

            if submission.visitor_email:
                email_lines.append(f"Email: {submission.visitor_email}")

            if submission.textbox:
                email_lines.extend(
                    [
                        "",
                        f"{form.textbox_prompt or 'Response'}:",
                        submission.textbox,
                    ]
                )

            if form.checkbox_prompt:
                checkbox_answer = "Yes" if submission.checkbox else "No"
                email_lines.append(f"{form.checkbox_prompt}: {checkbox_answer}")

            try:
                send_mail(
                    subject=f"New submission: {form.form_name}",
                    message="\n".join(email_lines),
                    from_email=None,
                    recipient_list=[form.user.email],
                    fail_silently=False,
                )
                email_sent = True
            except Exception:
                messages.error(
                    request,
                    "Email delivery failed. The submission was saved "
                    "so the response won't be lost.",
                )

    # Keep the submission permanently if database storage is enabled.
    # Otherwise, remove the temporary copy only after successful email.
    if not form.store_submissions and email_sent:
        submission.delete()

    if not form.email_submissions:
        messages.success(request, "Submission received successfully.")
    elif email_sent:
        messages.success(request, "Submission received and emailed successfully.")

    return redirect(redirect_view, username=username)
