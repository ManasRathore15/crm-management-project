from django.shortcuts import render, redirect
from . models import Lead

# Create your views here.

def home(request):

    sucess = False

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        city = request.POST.get('city')
        service = request.POST.get('service')

        Lead.objects.create(
            name=name,
            phone=phone,
            email=email,
            message=message,
            city=city,
            service=service
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