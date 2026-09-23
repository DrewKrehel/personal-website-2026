from django.contrib import admin

# Register your models here.
from builder.models import Profile, Project, Resume, Link, Form, FormSubmission

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Resume)
admin.site.register(Link)
admin.site.register(Form)
admin.site.register(FormSubmission)

