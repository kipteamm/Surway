from django.urls import path

from .views import *


urlpatterns = [
    path('forms', forms, name='forms'),
    path('forms/edit', edit_form, name='edit_form'),
    path('forms/answers', form_answers, name='form_answers'),
    path('form/<int:form_id>', form, name='form'),
]