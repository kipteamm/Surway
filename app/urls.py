from django.urls import path

from .views import *


urlpatterns = [
    path('forms', forms, name='forms'),
    path('forms/create', create_form, name='create_form'),
    path('forms/edit/<int:form_id>', edit_form, name='edit_form')
]