from django.shortcuts import render, redirect

from django.core.mail import send_mail

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.decorators import login_required

import csv
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator

from decouple import config

from .models import Lead, Agent
from django.shortcuts import get_object_or_404


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

        try:
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

                from_email=config('EMAIL_HOST_USER', default=''),

                recipient_list=[

                    'testmail071220002@gmail.com',


                ],

                fail_silently=False,

            )
        except Exception:
            pass


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

    search_query = request.GET.get('search', '')

    status_filter = request.GET.get('status', '')


    # GET ALL LEADS
    if request.user.is_superuser:
        all_leads = Lead.objects.all().order_by('-created_at')
    else:
        try:
            agent = Agent.objects.get(user=request.user)
            all_leads = Lead.objects.filter(agent=agent).order_by('-created_at')
        except Agent.DoesNotExist:
            all_leads =Lead.objects.none()



    # SEARCH

    if search_query:

        all_leads = all_leads.filter(

            Q(name__icontains=search_query) |

            Q(phone__icontains=search_query) |

            Q(email__icontains=search_query) |

            Q(city__icontains=search_query) |

            Q(service__icontains=search_query)

        )


    # STATUS FILTER

    if status_filter:

        all_leads = all_leads.filter(
            status=status_filter
        )


    # PAGINATION

    paginator = Paginator(all_leads, 10)

    page_number = request.GET.get('page')

    leads = paginator.get_page(page_number)


    # STATS

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

        'search_query': search_query,

        'status_filter': status_filter,

        'total_leads': total_leads,

        'new_leads': new_leads,

        'contacted_leads': contacted_leads,

        'in_progress_leads': in_progress_leads,

        'completed_leads': completed_leads,

        'rejected_leads': rejected_leads,

        'agents' : Agent.objects.all()

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



@login_required(login_url='/login/')
def export_csv(request):

    response = HttpResponse(content_type = 'text/csv')

    response['Content-Disposition'] = 'attachment ; filename= "leads.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'Name',
        'Phone',
        'Email',
        'City',
        'Service',
        'Status',
        'Created_at',
    ]) 


    leads = Lead.objects.all().order_by('-created_at')

    for lead in leads:
        writer.writerow([
            lead.name,
            lead.phone,
            lead.email,
            lead.city,
            lead.service,
            lead.status,
            lead.created_at
        ])

    return response



def assign_agent(request, lead_id):

    if request.method == 'POST':

        lead = get_object_or_404(Lead,id=lead_id)

        agent_id = request.POST.get('agent')

        if agent_id:
            agent = Agent.objects.get(id=agent_id)
            lead.agent = agent
            lead.save()

    return redirect('/dashboard/')



@login_required
def agents_view(request):
    agents = Agent.objects.all()
    return render(request, 'agents.html', {'agents': agents})


@login_required
def overview_view(request):
    total_leads = Lead.objects.count()
    completed = Lead.objects.filter(status='COMPLETED').count()

    context = {
        'total_leads': total_leads,
        'completed': completed,
    }

    return render(request, 'overview.html', context)