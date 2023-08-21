from django.shortcuts import render, redirect

from formapp import models


def forms(request):
    user = models.User.objects.filter(token=request.COOKIES.get('au_id'))

    if not user.exists():
        return redirect('/login')

    user = user.first()

    return render(request, 'app/forms.html')


def create_form(request):
    return render(request, 'app/create_form.html')


def edit_form(request):
    return render(request, 'app/edit_form.html')