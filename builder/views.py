from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import Profile
from .models import Project
from .models import Resume
from .models import Link
from .models import Form
from .models import FormSubmission
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def home(request, username):
    profile = Profile.objects.get(user__username=username)
    
    context = {
        'profile': profile,
    }
    
    return render(request, 'index.html', context=context)

def about_me(request, username):
    profile = Profile.objects.get(user__username=username)
    
    context = {
        'profile': profile,
    }
    
    return render(request, 'about_me.html', context=context)

def projects(request, username):
    projects = Project.objects.filter(user__username=username)
    profile = Profile.objects.get(user__username=username)

    
    context = {
        'projects': projects,
        'profile': profile,
    }
    
    return render(request, 'projects.html', context=context)

def resumes(request, username):
    resumes = Resume.objects.filter(user__username=username)
    profile = Profile.objects.get(user__username=username)

    
    context = {
        'resumes': resumes,
        'profile': profile,
    }
    
    return render(request, 'resumes.html', context=context)

def links(request, username):
    links = Link.objects.filter(user__username=username)
    profile = Profile.objects.get(user__username=username)

    
    context = {
        'links': links,
        'profile': profile,
    }
    
    return render(request, 'links.html', context=context)

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
            )
        )
        for form in forms
    ]

    context = {
        'form_pairs': form_pairs,
        'profile': profile,
    }
    
    return render(request, 'forms.html', context=context)

def form_submit(request, username):
    if request.method != "POST":
        messages.error(request, "Invalid request.")
        return redirect("forms", username=username)
    
    form_id = request.POST.get("form_id")
    if not form_id:
        messages.error(request, "We couldn't identify the form you submitted.")
        return redirect("forms", username=username)
    try:
        form = Form.objects.get(
            id=form_id,
            user__username=username,
        )
    except Form.DoesNotExist:
        messages.error(request, "That form is no longer available.")
        return redirect("forms", username=username)
    
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
        return redirect("forms", username=username)
    
    
    submission = FormSubmission(
        form=form,
        visitor_name=contact_form.cleaned_data.get("visitor_name"),
        visitor_email=contact_form.cleaned_data.get("visitor_email"),
        textbox=contact_form.cleaned_data.get("textbox"),
        checkbox=contact_form.cleaned_data.get("checkbox"),
    )
    submission.save()
    messages.success(request, "Submission success!")
    return redirect("forms", username=username)