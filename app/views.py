from django.shortcuts import render, redirect
from django.contrib import messages

from formapp import models

from .form_data import CreateFormFormData

from api import functions


def forms(request):
    user = models.User.objects.filter(token=request.COOKIES.get('au_id'))

    if not user.exists():
        return redirect('/login')

    user = user.first()

    user_forms = models.Form.objects.filter(user_id=user.id) # type: ignore

    return render(request, 'app/forms.html', {
        'user_forms' : user_forms
    })


def create_form(request):
    user = models.User.objects.filter(token=request.COOKIES.get('au_id'))

    if not user.exists():
        return redirect('/login')
    
    user = user.first()
    
    if request.method == "POST":
        form_data = CreateFormFormData(request.POST)

        if form_data.is_valid():
            form = functions.create_form(user.id, form_data.cleaned_data) # type: ignore

            if isinstance(form, models.Form):
                return redirect(f'/forms/edit?id={form.id}')
            
            messages.error(request, "Unknown issue occured")

            return redirect('/forms/create')
    else:
        form_data = CreateFormFormData()
    
    return render(request, 'app/create_form.html', {
        "form" : form_data
    })


def edit_form(request):
    user = models.User.objects.filter(token=request.COOKIES.get('au_id'))

    if not user.exists():
        return redirect('/login')
    
    user = user.first()

    form = models.Form.objects.filter(user_id=user.id, id=request.GET.get('id')) # type: ignore

    if not form.exists():
        messages.error(request, "Form not found")

        return redirect('/forms')
    
    form = form.first()

    response = render(request, 'app/edit_form.html', {
        'form' : form,
        'questions' : models.Question.objects.filter(form_id=form.id).order_by('index') # type: ignore
    })

    response.set_cookie('ef_id', form.id) # type: ignore

    return response


def form(request, form_id):
    form = models.Form.objects.filter(id=form_id) # type: ignore

    if not form.exists():
        messages.error(request, "Form not found")

        return redirect('/forms')
    
    form = form.first()

    if form.require_login: # type: ignore
        user = models.User.objects.filter(token=request.COOKIES.get('au_id'))

        if not user.exists():
            return redirect(f'/login?next=/form/{form_id}')
        
        user = user.first()

    response = render(request, 'app/form.html', {
        'form' : form,
        'questions' : models.Question.objects.filter(form_id=form.id).order_by('index') # type: ignore
    })

    response.set_cookie('ef_id', form.id) # type: ignore

    return response