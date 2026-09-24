from django.shortcuts import render
from .models import Profile

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