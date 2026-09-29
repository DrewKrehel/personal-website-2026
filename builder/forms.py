from django import forms

class ContactForm(forms.Form):
    visitor_name = forms.CharField()
    visitor_email = forms.EmailField()