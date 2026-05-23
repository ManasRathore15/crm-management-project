from django.shortcuts import render, redirect

from django.core.mail import send_mail

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.decorators import login_required

from decouple import config

from .models import Lead


# HOME PAGE

def home(request):

    if request.method == 'POST':

        name = request.POST.get('name')

        phone = request.POST.get('phone')

        email = request.POST.get('email')

        city = request.POST.get('city')

        service = request.POST.get('service')

        message = request.POST.get('message')


        # PHONE VALIDATION

        if not phone.isdigit():

            return render(

                request,

                'home.html',

                {
                    'error': 'Phone number must contain only digits'
                }

            )


        if len(phone) != 10:

            return render(

                request,

                'home.html',

                {
                    'error': 'Phone number must be exactly 10 digits'
                }

            )


        if not phone.startswith(('6', '7', '8', '9')):

            return render(

                request,

                'home.html',

                {
                    'error': 'Enter a valid Indian mobile number'
                }

            )


        # SAVE LEAD

        Lead.objects.create(

            name=name,

            phone=phone,

            email=email,

            city=city,

            service=service,

            message=message

        )


        # EMAIL NOTIFICATION

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


# LOGIN PAGE

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

            error = 'Invalid Username or Password'


    context = {

        'error': error

    }


    return render(

        request,

        'login.html',

        context

    )


# DASHBOARD

@login_required(login_url='/login/')
def dashboard_view(request):

    leads = Lead.objects.all().order_by('-created_at')

    total_leads = Lead.objects.count()

    new_leads = Lead.objects.filter(
        status='NEW'
    ).count()

    contacted_leads = Lead.objects.filter(
        status='CONTACTED'
    ).count()

    in_progress_leads = Lead.objects.filter(
        status='IN_PROGRESS'
    ).count()

    completed_leads = Lead.objects.filter(
        status='COMPLETED'
    ).count()

    rejected_leads = Lead.objects.filter(
        status='REJECTED'
    ).count()


    context = {

        'leads': leads,

        'total_leads': total_leads,

        'new_leads': new_leads,

        'contacted_leads': contacted_leads,

        'in_progress_leads': in_progress_leads,

        'completed_leads': completed_leads,

        'rejected_leads': rejected_leads

    }

    return render(

        request,

        'dashboard.html',

        context

    )


def update_status(request, lead_id):
    if request.method == 'POST':
        lead = Lead.objects.get(id=lead_id)
        new_status = request.POST.get('status')
        lead.status = new_status
        lead.save()

    return redirect('/dashboard/')


# LOGOUT

def logout_view(request):

    logout(request)

    return redirect('/login/')