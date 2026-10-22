from urllib.parse import parse_qs, urlparse
import re
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Model representing a profile page"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    featured_section = models.CharField(
        max_length=20,
        choices=[
            ("about", "About Me"),
            ("projects", "Projects"),
            ("resumes", "Resumes"),
            ("links", "Links"),
            ("forms", "Forms"),
        ],
        blank=True,
    )

    featured_object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
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

    index_thumbnail = models.ImageField(
        upload_to="index_thumbnails/",
        blank=True,
    )

class Project(models.Model):
    """Model representing a portfolio page"""

    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200,
        help_text="Enter the name of your project"
    )

    description = models.TextField(
        max_length=500,
        blank=True,
        help_text="Enter a brief description of your project"
    )

    link = models.URLField(
        help_text="Enter the URL for your project"
    )

    image = models.ImageField(
        upload_to='project_images/',
        blank=True,
        help_text="Upload a project image"
    )

    video_url = models.URLField(
        blank=True,
        help_text="Optional YouTube or Vimeo URL to embed instead of the thumbnail image",
    )

    sort_order = models.PositiveIntegerField(default=0)
    
    def get_video_embed_url(self):
        if not self.video_url:
            return ""

        parsed_url = urlparse(self.video_url)
        host = parsed_url.hostname or ""
        path_parts = [part for part in parsed_url.path.split("/") if part]

        # YouTube videos
        if host in {
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
            "youtube-nocookie.com",
            "www.youtube-nocookie.com",
        }:
            if parsed_url.path == "/watch":
                video_id = parse_qs(parsed_url.query).get("v", [""])[0]
            elif len(path_parts) >= 2 and path_parts[0] in {
                "embed", "shorts", "live"
            }:
                video_id = path_parts[1]
            else:
                return ""

            if re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
                return f"https://www.youtube-nocookie.com/embed/{video_id}"

        elif host in {"youtu.be", "www.youtu.be"}:
            video_id = path_parts[0] if path_parts else ""

            if re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
                return f"https://www.youtube-nocookie.com/embed/{video_id}"

        # Vimeo videos
        elif host in {"vimeo.com", "www.vimeo.com"}:
            video_id = path_parts[0] if path_parts else ""

            if video_id.isdigit():
                return f"https://player.vimeo.com/video/{video_id}"

        elif host == "player.vimeo.com":
            if len(path_parts) == 2 and path_parts[0] == "video":
                video_id = path_parts[1]

                if video_id.isdigit():
                    return f"https://player.vimeo.com/video/{video_id}"

        return ""

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
    
    sort_order = models.PositiveIntegerField(default=0)

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
    
    is_social = models.BooleanField(
        default=False,
        help_text="Display this link in the homepage social icon banner"
    )
    
    link_image = models.ImageField(
        upload_to='link_images/',
        blank=True,
        help_text="Upload a link icon or image"
    )
    sort_order = models.PositiveIntegerField(default=0)

class Form(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    form_name = models.CharField(
        max_length=200,
        help_text="Enter the name of your form"
    )
    
    store_submissions = models.BooleanField(
        default=True,
        help_text="Save responses in the dashboard"
    )

    email_submissions = models.BooleanField(
        default=False,
        help_text="Email responses to your account email address"
    )
    
    include_name = models.BooleanField(default=False)
    name_required = models.BooleanField(default=False)
    include_email = models.BooleanField(default=False)
    email_required = models.BooleanField(default=False)
  

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
    
    sort_order = models.PositiveIntegerField(default=0)

class FormSubmission(models.Model):
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE
    )

    visitor_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Enter your name"
    )  

    visitor_email = models.EmailField(
        max_length=200,
        blank=True,
        null=True,
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
