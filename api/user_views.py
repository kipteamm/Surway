from django.core.cache import cache

from rest_framework.decorators import api_view
from rest_framework import status

from .request_handler import HandleRequest, CredentialTypes, DefaultTypes, StringTypes

from formapp import models

import sys


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

    for form in models.Form.objects.filter(user_id=user.id):
        total_size += sys.getsizeof(form)

    for question in models.Question.objects.filter(user_id=user.id):
        total_size += sys.getsizeof(question)

    total_size = {
        'total_size' : total_size
    }

    cache.set(cache_key, total_size, timeout=None)

    response.data = total_size

    return response.build()

    