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
    contact_form = ContactForm()

    
    context = {
        'forms': forms,
        'profile': profile,
        'contact_form' : contact_form,
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
    submission = FormSubmission(
        form=form,
        visitor_name=request.POST.get("visitor_name"),
        visitor_email=request.POST.get("visitor_email"),
        textbox=request.POST.get("textbox"),
        checkbox="checkbox" in request.POST
    )
    submission.save()
    messages.success(request, "Submission success!")
    return redirect("forms")