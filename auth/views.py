from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

from commons import functions 

from formapp import models

import time


def register(request):
    if request.method == "POST":
        email_address = request.POST.get('email_address')

        if models.User.objects.filter(email_address__iexact=email_address).exists():
            messages.error(request, "Account already exists")

            return redirect('register')

        password = request.POST.get('password')

        salt = functions.random_string(255)

        models.User.objects.create(
            email_address=email_address,
            password=functions.sha256(f"{salt}${password}"),
            salt=salt,
            creation_timestamp=time.time()
        )

        messages.success(request, "Account successfully created")

        return redirect('/login')

    return render(request, 'auth/register.html')


def login(request):
    if request.method == "POST":
        email_address = request.POST.get('email_address')
        password = request.POST.get('password')

        user = models.User.objects.get(email_address__iexact=email_address)

        if functions.path_exists(request.GET.get('next')):
            next_page = request.GET.get('next')
        else:
            next_page = '/forms'

        if functions.sha256(f"{user.salt}${password}") != user.password:
            messages.error(request, "Invalid password")

            if next_page != '/forms':
                return redirect(f'/login?next={next_page}')
        
            return redirect('/login')
        
        user.token = functions.sha256(f"token${time.time()}")
        user.save()
        
        messages.success(request, "Logged in")

        response = redirect(next_page)
        response.set_cookie('au_id', user.token)

        return response
    
    return render(request, 'auth/login.html')


def test(request):
    for user in models.User.objects.all():
        user.delete()

    return HttpResponse('success')