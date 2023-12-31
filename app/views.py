from django.shortcuts import render, redirect
from django.contrib import messages

from authentication.models import User

from app.models import Form, Question

from utils.decorators import requires_login
from utils import snowflakes

from api import request_handler

from .forms import CaptchaForm


@requires_login
def forms(request):
    user = request.user

    return render(request, 'app/forms.html', {
        'user_forms' : Form.objects.filter(user=user).order_by('-last_edit_timestamp'), # type: ignore
        'user' : user,
    })


@requires_login
def edit_form(request):
    user = request.user

    form = Form.objects.filter(user=user, id=request.GET.get('id')) # type: ignore

    if not form.exists():
        messages.error(request, "Form not found")

        return redirect('/forms')
    
    form = form.first()

    response = render(request, 'app/edit_form.html', {
        'form' : form,
        'user' : user,
        'questions' : Question.objects.filter(form=form).order_by('index') # type: ignore
    })

    response.set_cookie('ef_id', form.id) # type: ignore

    return response


@requires_login
def form_answers(request):
    user = request.user

    form = Form.objects.filter(user=user, id=request.GET.get('id')) # type: ignore

    if not form.exists():
        messages.error(request, "Form not found")

        return redirect('/forms')
    
    form = form.first()

    questions = Question.objects.filter(form=form).order_by('index') # type: ignore

    questions_data = []

    for question in questions:
        questions_data.append(question.to_dict(False, True))

    response = render(request, 'app/form_answers.html', {
        'form' : form,
        'user' : user,
        'questions' : questions_data,
    })

    response.set_cookie('ef_id', form.id) # type: ignore

    return response


def form(request, form_id):
    user = User.objects.filter(token=request.COOKIES.get('au_id'))
    form = Form.objects.filter(id=form_id) # type: ignore

    if user:
        user = user.first()

    if not form.exists():
        return render(request, 'app/form_not_found.html', {
            'user' : user
        })
    
    form = form.first()

    questions = Question.objects.filter(form=form).order_by('index') # type: ignore

    if not questions:
        return render(request, 'app/empty_form.html', {
            'user' : user
        })

    if form.require_account: # type: ignore
        if not user:
            return redirect(f'/login?next=/form/{form_id}')
        
    track_id = request.GET.get('track_id')

    if track_id:
        if request_handler.StringTypes(track_id).is_valid(request_handler.StringTypes.TRACK_ID):
            track_id = None
    
    if not track_id:
        track_id = str(snowflakes.SnowflakeGenerator().generate_id())

    if not user:
        captcha = CaptchaForm()
    else:
        captcha = None
            

    response = render(request, 'app/form.html', {
        'form' : form,
        'user' : user,
        'questions' : questions, 
        'track_id' : track_id,
        'captcha' : captcha
    })

    return response