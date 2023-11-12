from django.core.cache import cache

from rest_framework.decorators import api_view

from .request_handler import HandleRequest, CredentialTypes

from authentication.models import User

from app.models import Form, Question

import sys


@api_view(('GET', ))
def get_user(request, email_address):
    handle_request = HandleRequest(request, [email_address])
    response = handle_request.has_parameters([CredentialTypes.EMAIL_ADDRESS])\
    
    if not response.ok:
        return response.build()
    
    user = User.objects.get(email_address__iexact=email_address)

    response.data = user.to_dict()

    return response.build()


@api_view(('GET', ))
def get_user_storage(request):
    handle_request = HandleRequest(request)
    response = handle_request.is_authenticated()

    if not response.ok:
        return response.build()
    
    user = response.user

    cache_key = f"total_storage:{user.id}"

    total_size = cache.get(cache_key)

    if total_size:
        response.data = total_size

        return response.build()

    total_size = 0

    for form in Form.objects.filter(user_id=user.id):
        total_size += sys.getsizeof(form)

    for question in Question.objects.filter(user_id=user.id):
        total_size += sys.getsizeof(question)

    total_size = {
        'total_size' : total_size / 1024 / 1024
    }

    cache.set(cache_key, total_size, timeout=None)

    response.data = total_size

    return response.build()

    