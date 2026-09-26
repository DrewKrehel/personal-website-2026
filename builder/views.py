from django.shortcuts import render
from .models import Profile
from .models import Project
from .models import Resume
from .models import Link

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