from django import forms

class ContactForm(forms.Form):
    def __init__(self, textbox_prompt=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if textbox_prompt:
            self.fields["textbox"].label = textbox_prompt
    
    visitor_name = forms.CharField()
    visitor_email = forms.EmailField()
    textbox = forms.CharField(label="What do you think?")
    checkbox = forms.BooleanField(required=False)
    
