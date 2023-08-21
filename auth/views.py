from django.shortcuts import render, redirect
from django.contrib import messages

from commons import functions 

from formapp import models

import time


def register(request):
    if request.method == "POST":
        email_address = request.POST.get('email_address')
        password = request.POST.get('password')

        salt = functions.random_string(255)

        models.User.objects.create(
            email_address=email_address,
            password=functions.sha256(f"{salt}${password}"),
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

        if functions.sha256(f"{user.salt}${password}") != user.password:
            messages.error(request, "Invalid password")

            return redirect('/forms')
        
        user.token = functions.sha256(f"token${time.time()}")
        
        messages.success(request, "Logged in")
        
        response = redirect('/forms')
        response.set_cookie('au_id', user.token)

        return response
    
    return render(request, 'auth/login.html')