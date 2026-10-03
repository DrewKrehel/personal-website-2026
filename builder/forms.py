from django import forms

class ContactForm(forms.Form):
    visitor_name = forms.CharField()
    visitor_email = forms.EmailField()
    
    def __init__(self, *args, textbox_prompt=None, checkbox_prompt=None, **kwargs):
        super().__init__(*args, **kwargs)
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
