from .exceptions import Exceptions

from surway import models

from typing import Union

import time

def create_form(user_id, data: dict) -> Union[Exceptions, models.Form]:
    title = data['title']

    if len(title) > 100:
        return Exceptions.MAX_LENGTH_EXCEEDED
    
    description = None

    if 'description' in data:
        description = data['description']

        if len(description) > 1000:
            return Exceptions.MAX_LENGTH_EXCEEDED
    
    form = models.Form.objects.create(
        user_id=user_id,
        title=title,
        description=description,
        creation_timestamp=time.time(),
        last_edit_timestamp=time.time()
    )

    return form