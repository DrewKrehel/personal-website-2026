from django.shortcuts import render
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

    
    context = {
        'forms': forms,
        'profile': profile,
    }
    
    return render(request, 'forms.html', context=context)

def form_submit(request):
    if request.method == "POST":
        print(request.POST)
        form = Form.objects.get(id=request.POST["form_id"])
        submission = FormSubmission(
            form=form,
            visitor_name=request.POST["visitor_name"],
            visitor_email=request.POST["visitor_email"],
            textbox=request.POST["textbox"],
            checkbox="checkbox" in request.POST
        )
        submission.save()
        return HttpResponse("Form submission received!")
    else:
        return HttpResponse("Invalid request")

# def form_submissions(request):
#     form_submissions = FormSubmission.objects.filter(user__username="drewkrehel")
#     profile = Profile.objects.get(user__username="drewkrehel")

    
#     context = {
#         'form_submissions': form_submissions,
#         'profile': profile,
#     }
    
#     return render(request, 'form_submissions.html', context=context)

