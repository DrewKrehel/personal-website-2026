from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Model representing a profile page"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    display_name = models.CharField(
        max_length=200,
        help_text="Enter the name you want visitors to see"
    )

    email = models.EmailField(
        max_length=200,
        help_text="Enter the email you want visitors to see"
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
        help_text="Enter the # you want visitors to see"
    )

    bio = models.TextField(
        max_length=1000,
        blank=True,
        help_text="Add a short bio"
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        help_text="Upload a profile image"
    )

class Project(models.Model):
    """Model representing a portfolio page"""

    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE
    )

    project_title = models.CharField(
        max_length=200,
        help_text="Enter the name of your project"
    )

    project_description = models.TextField(
        max_length=500,
        blank=True,
        help_text="Enter a brief description of your project"
    )

    project_link = models.URLField(
        help_text="Enter the URL for your project"
    )

    project_image = models.ImageField(
        upload_to='project_images/',
        blank=True,
        help_text="Upload a project image"
    )

class Resume(models.Model):
    """Model representing a resume"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    display_name = models.CharField(
        max_length=200,
        help_text="Enter the name or purpose of your resume"
    )

    file = models.FileField(
        upload_to='resumes/',
        help_text="Upload your resume file"
    )

class Link(models.Model):
    """Model representing a website link"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    display_name = models.CharField(
        max_length=200,
        help_text="Enter the name of your link"
    )
    
    link_url = models.URLField(
        help_text="Enter the URL for your link"
    )
    
    link_image = models.ImageField(
        upload_to='link_images/',
        blank=True,
        help_text="Upload a link icon or image"
    )

class Form(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    display_name = models.CharField(
        max_length=200,
        help_text="Enter the name of your form"
    )  

    textbox_prompt = models.TextField(
        max_length=700,
        blank=True,
        help_text="Describe the question or purpose of this field"
    )

    checkbox_prompt = models.TextField(
        max_length=700,
        blank=True,
        help_text="Describe the question or purpose of this field"
    )

    outro = models.TextField(
        max_length=500,
        blank=True,
        help_text="Leave a message or reminder for your form"
    )

class FormSubmission(models.Model):
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE
    )

    visitor_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Enter your name"
    )  

    visitor_email = models.EmailField(
        max_length=200,
        blank=True,
        help_text="Enter your email"
    )  

    textbox = models.TextField(
        max_length=700,
        blank=True,
        help_text="Answer the prompt"
    )

    checkbox = models.BooleanField(
        default=False,
    )

