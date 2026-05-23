from django.shortcuts import render, redirect
from django.core.mail import send_mail
from decouple import config
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
                'testmail071220002@gmail.com',
                'avdeshkharadiya77@gmail.com'
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

def login_view(request):
    
    
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        
        else:
            error = "Invalid Username or Password"

    contex = {
        "error" : error
    }

    return render(
        request,
        'login.html',
        contex

    )



def dashboard_view(request):
    leads = Lead.objects.all().order_by('-id')

    contex = {
        'leads': leads

    }

    return render(
        request,
        'dashboard.html',
        contex

    )


def logout_view(request):
    logout(request)

    return redirect("/login/")