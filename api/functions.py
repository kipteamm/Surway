from .exceptions import Exceptions

from authentication.models import User

from app.models import Form

from typing import Union

import time


def create_form(user: User, data: dict) -> Union[Exceptions, Form]:
    title = data['title']

    if len(title) > 100:
        return Exceptions.MAX_LENGTH_EXCEEDED
    
    description = None

    if 'description' in data:
        description = data['description']

        if len(description) > 1000:
            return Exceptions.MAX_LENGTH_EXCEEDED
    
    form = Form.objects.create(
        user=user,
        title=title,
        description=description,
        creation_timestamp=time.time(),
        last_edit_timestamp=time.time()
    )

    return form