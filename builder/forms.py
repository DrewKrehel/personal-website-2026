from urllib.parse import urlparse
from django import forms
from .models import Profile, Project, Resume, Link, Form

class ContactForm(forms.Form):
    def __init__(
        self,
        *args,
        include_name=False,
        name_required=False,
        include_email=False,
        email_required=False,
        textbox_prompt=None,
        checkbox_prompt=None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        if include_name:
            self.fields["visitor_name"] = forms.CharField(
                label="Visitor name",
                required=name_required,
            )

        if include_email:
            self.fields["visitor_email"] = forms.EmailField(
                label="Visitor email",
                required=email_required,
            )

        if textbox_prompt:
            self.fields["textbox"] = forms.CharField(
                label=textbox_prompt,
                required=False,
            )

        if checkbox_prompt:
            self.fields["checkbox"] = forms.BooleanField(
                label=checkbox_prompt,
                required=False,
            ) 

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is None:
            return

        section = (
            self.data.get("featured_section")
            or self.instance.featured_section
        )

        if section == "about":
            self.fields["featured_object_id"].choices = [
                ("", "Nothing selected"),
            ]

            if self.is_bound:
                self.data = self.data.copy()
                self.data["featured_object_id"] = ""

        if section == "about":
            self.initial["featured_object_id"] = None

        print("Featured section:", repr(section))

        if section == "projects":
            objects = Project.objects.filter(user=user)
            choices = [(obj.id, obj.title) for obj in objects]

        elif section == "resumes":
            objects = Resume.objects.filter(user=user)
            choices = [(obj.id, obj.display_name) for obj in objects]

        elif section == "links":
            objects = Link.objects.filter(user=user)
            choices = [(obj.id, obj.display_name) for obj in objects]

        elif section == "forms":
            objects = Form.objects.filter(user=user)
            choices = [(obj.id, obj.form_name) for obj in objects]

        else:
            choices = []

        self.fields["featured_object_id"].choices = [
            ("", "Nothing selected"),
            *choices,
        ]

    featured_section = forms.ChoiceField(
        choices=[
            ("", "Nothing featured"),
            ("about", "About Me"),
            ("projects", "Projects"),
            ("resumes", "Resumes"),
            ("links", "Links"),
            ("forms", "Forms"),
        ],
        required=False,
        label="Featured section",
    )

    featured_object_id = forms.TypedChoiceField(
        choices=[("", "Nothing selected")],
        required=False,
        coerce=int,
        empty_value=None,
        label="Featured object",
    )
    class Meta:
        model = Profile
        fields = [
            "display_name",
            "email",
            "phone",
            "bio",
            "profile_image",
            "index_thumbnail",
            "featured_section",
            "featured_object_id",
        ]

class ProjectForm(forms.ModelForm):
    
    def clean_video_url(self):
        video_url = self.cleaned_data.get("video_url", "").strip()

        if not video_url:
            return ""

        parsed_url = urlparse(video_url)
        allowed_hosts = {
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
            "youtu.be",
            "www.youtu.be",
            "youtube-nocookie.com",
            "www.youtube-nocookie.com",
            "vimeo.com",
            "www.vimeo.com",
            "player.vimeo.com",
        }

        if parsed_url.scheme != "https" or parsed_url.hostname not in allowed_hosts:
            raise forms.ValidationError(
                "Enter a valid HTTPS YouTube or Vimeo video URL."
            )

        return video_url
    
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "link",
            "image",
            "video_url",
        ]

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'display_name',
            'file',
        ]

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = [
            'display_name',
            'link_url',
            'link_image',
            'is_social',
        ]

class FormBuilderForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = [
            "form_name",
            "store_submissions",
            "email_submissions",
            "include_name",
            "name_required",
            "include_email",
            "email_required",
            "textbox_prompt",
            "checkbox_prompt",
            "outro",
        ]

    def clean(self):
        cleaned_data = super().clean()

        store_submissions = cleaned_data.get("store_submissions")
        email_submissions = cleaned_data.get("email_submissions")

        if not store_submissions and not email_submissions:
            raise forms.ValidationError(
                "You must enable database storage, email delivery, or both."
            )

        return cleaned_data


class IndexThumbnailForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["index_thumbnail"]
