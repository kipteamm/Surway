from django.shortcuts import render, redirect
from django.contrib import messages

from surway import models

from api import request_handler


def forms(request):
    user = models.User.objects.filter(token=request.COOKIES.get('au_id'))

    if not user.exists():
        return redirect('/login')

    user = user.first()

    user_forms = models.Form.objects.filter(user_id=user.id) # type: ignore

    return render(request, 'app/forms.html', {
        'user_forms' : user_forms,
        'user' : user,
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
        'user' : user,
        'questions' : models.Question.objects.filter(form_id=form.id).order_by('index') # type: ignore
    })

    response.set_cookie('ef_id', form.id) # type: ignore

    return response


def form_answers(request):
    user = models.User.objects.filter(token=request.COOKIES.get('au_id'))

    if not user.exists():
        return redirect('/login')
    
    user = user.first()

    form = models.Form.objects.filter(user_id=user.id, id=request.GET.get('id')) # type: ignore

    if not form.exists():
        messages.error(request, "Form not found")

        return redirect('/forms')
    
    form = form.first()

    response = render(request, 'app/form_answers.html', {
        'form' : form,
        'user' : user,
        'questions' : models.Question.objects.filter(form_id=form.id).order_by('index'), # type: ignore
        'answers' : models.Answer.objects.filter(form_id=form.id) # type: ignore
    })

    response.set_cookie('ef_id', form.id) # type: ignore

    return response


def form(request, form_id):
    user = models.User.objects.filter(token=request.COOKIES.get('au_id'))
    form = models.Form.objects.filter(id=form_id) # type: ignore

    if user:
        user = user.first()

    if not form.exists():
        return render(request, 'app/form_not_found.html', {
            'user' : user
        })
    
    form = form.first()

    if form.require_account: # type: ignore
        if not user:
            return redirect(f'/login?next=/form/{form_id}')
        
    track_id = request.GET.get('track_id')

    if track_id:
        if request_handler.StringTypes(track_id).is_valid(request_handler.StringTypes.TRACK_ID):
            track_id = None

    response = render(request, 'app/form.html', {
        'form' : form,
        'user' : user,
        'questions' : models.Question.objects.filter(form_id=form.id).order_by('index'), # type: ignore
        'track_id' : track_id
    })

    return response