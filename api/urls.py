from django.urls import path

from .form_views import *
from .user_views import *


urlpatterns = [
    # Users
    path('user/<str:email_address>', get_user, name='get_user'),
    path('user/storage', get_user_storage, name='get_user_storage'),
    

    # Forms
    path('form/create', create_form, name='create_form'),
    path('form/update', update_form, name='update_form'),
    path('form/delete/<int:form_id>', delete_form, name='delete_form'),

    path('question/create', create_question, name='create_question'),
    path('question/update', update_question, name='update_question'),

    path('answer/submit', submit_answer, name='submit_answer'),
]