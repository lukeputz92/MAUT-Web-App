from django import forms
from django.forms.formsets import formset_factory, BaseFormSet

#All the information used in the 'Contact Us' page.
class ContactForm(forms.Form):
    contact_name = forms.CharField(label = "Name",required=True,
                                widget = forms.TextInput(attrs={
                                'placeholder':'Name'
                                }))
    contact_email = forms.EmailField(label = "Email",required=False,
                                widget = forms.TextInput(attrs={
                                    'placeholder': 'Email (optional)'
                                    }))
    content = forms.CharField(label = "Message",
        required=True,
        widget=forms.Textarea(attrs={
                                'placeholder': 'Message'
                              })
    )