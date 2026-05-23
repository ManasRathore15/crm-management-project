from django.shortcuts import render, redirect
from django.core.mail import send_mail
from decouple import config

from .models import Lead


def home(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        city = request.POST.get('city')
        service = request.POST.get('service')
        message = request.POST.get('message')

        # Save Lead in Database

        Lead.objects.create(

            name=name,
            phone=phone,
            email=email,
            city=city,
            service=service,
            message=message

        )

        # Send Email Notification

        send_mail(

            subject='New Lead Submitted',

            message=f'''

New enquiry received

Name: {name}

Phone: {phone}

Email: {email}

City: {city}

Service: {service}

Message: {message}

''',

            from_email=config('EMAIL_HOST_USER'),

            recipient_list=[
                'testmail071220002@gmail.com'
            ],

            fail_silently=False,

        )

        return redirect('/?success=true')

    success = request.GET.get('success')

    context = {

        'success': success

    }

    return render(

        request,
        'home.html',
        context

    )