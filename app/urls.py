from django.urls import path

from .views import *


urlpatterns = [
    path('forms', forms, name='forms'),
    path('forms/edit', edit_form, name='edit_form'),
    path('form/<int:form_id>', form, name='form')
]