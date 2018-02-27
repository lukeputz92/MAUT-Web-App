from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from .forms import *
from django.core.mail import EmailMessage, send_mail, BadHeaderError



# Create your views here.

def example(request):
    if request.method == 'POST':
        contactForm = ContactForm(request.POST)
        if contactForm.is_valid():
            subject = "MAUT Contact Form Submission"
            message_content = contactForm.cleaned_data['content']
            if contactForm.cleaned_data['contact_email']:
                from_email = contactForm.cleaned_data['contact_email']
            else:
                from_email = "n/a"

            message = "***This message is an automatically generated message from MAUT's contact page***\n" + "Name: " + contactForm.cleaned_data['contact_name'] + "\n" + "Email Address: " + from_email + "\n" + "Message: " + message_content + "\n"

            try:
                send_mail(subject, message, from_email, ['markamay@live.com','MAUtilityTheory@gmail.com','mark.brown8790@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request,'contact/thankyou.html', {})
        else:
            return render(request,'contact/contact.html', {'form': ContactForm()})

    else:
        contactForm = ContactForm()

    # return render(request,'contact/contact.html', {'form': ContactForm()})

    return render(request, 'example/index.html', {'form': ContactForm()})