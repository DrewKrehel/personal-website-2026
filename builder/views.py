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

def home(request):
    profile = Profile.objects.get(user__username="drewkrehel")
    
    context = {
        'profile': profile,
    }
    
    return render(request, 'index.html', context=context)

def about_me(request):
    profile = Profile.objects.get(user__username="drewkrehel")
    
    context = {
        'profile': profile,
    }
    
    return render(request, 'about_me.html', context=context)

def projects(request):
    projects = Project.objects.filter(user__username="drewkrehel")
    profile = Profile.objects.get(user__username="drewkrehel")

    
    context = {
        'projects': projects,
        'profile': profile,
    }
    
    return render(request, 'projects.html', context=context)

def resumes(request):
    resumes = Resume.objects.filter(user__username="drewkrehel")
    profile = Profile.objects.get(user__username="drewkrehel")

    
    context = {
        'resumes': resumes,
        'profile': profile,
    }
    
    return render(request, 'resumes.html', context=context)

def links(request):
    links = Link.objects.filter(user__username="drewkrehel")
    profile = Profile.objects.get(user__username="drewkrehel")

    
    context = {
        'links': links,
        'profile': profile,
    }
    
    return render(request, 'links.html', context=context)

def forms(request):
    forms = Form.objects.filter(user__username="drewkrehel")
    profile = Profile.objects.get(user__username="drewkrehel")
    form_pairs = [
        (
            form,
            ContactForm(
                textbox_prompt=form.textbox_prompt,
                checkbox_prompt=form.checkbox_prompt,
            )
        )
        for form in forms
    ]

    context = {
        'form_pairs': form_pairs,
        'profile': profile,
    }
    
    return render(request, 'forms.html', context=context)

def form_submit(request):
    if request.method != "POST":
        messages.error(request, "Invalid request.")
        return redirect("forms")
    
    form_id = request.POST.get("form_id")
    if not form_id:
        messages.error(request, "We couldn't identify the form you submitted.")
        return redirect("forms")
    try:
        form = Form.objects.get(id=form_id)
    except Form.DoesNotExist:
        messages.error(request, "That form is no longer available.")
        return redirect("forms")
    
    contact_form = ContactForm(
        request.POST,
        textbox_prompt=form.textbox_prompt,
        checkbox_prompt=form.checkbox_prompt,
        )
    
    if not contact_form.is_valid():
        messages.error(request, "Please correct the errors in the form.")
        return redirect("forms")
    
    
    submission = FormSubmission(
        form=form,
        visitor_name=contact_form.cleaned_data["visitor_name"],
        visitor_email=contact_form.cleaned_data["visitor_email"],
        textbox=contact_form.cleaned_data["textbox"],
        checkbox=contact_form.cleaned_data["checkbox"]
    )
    submission.save()
    messages.success(request, "Submission success!")
    return redirect("forms")