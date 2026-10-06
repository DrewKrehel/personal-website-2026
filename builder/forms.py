from django import forms

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