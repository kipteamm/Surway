from django.urls import path

from .form_views import *
from .user_views import *


urlpatterns = [
    # Users
    path('user/storage', get_user_storage, name='get_user_storage'),

    # Forms
    path('question/create', create_question, name='create_question'),
    path('question/update', update_question, name='update_question'),
]