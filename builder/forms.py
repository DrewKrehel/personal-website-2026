from django import forms
from .models import Profile, Project, Resume, Link

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
    class Meta:
        model = Profile
        fields = [
            'display_name',
            'email',
            'phone',
            'bio',
            'profile_image',
        ]

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'link',
            'image',
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
        ]