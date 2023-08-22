from django.urls import path

from .form_views import *


urlpatterns = [
    path('question/create', create_question, name='create_question')
]