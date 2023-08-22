from rest_framework.decorators import api_view
from rest_framework import status

from .request_handler import HandleRequest, CredentialTypes, DefaultTypes, StringTypes

from surway import models

import time


@api_view(('POST', ))
def create_form(request):
    handle_request = HandleRequest(request)
    response = handle_request.is_authenticated()

    if not response.ok:
        return response.build()

    parameters = handle_request.has_parameters([StringTypes.FORM_TITLE, DefaultTypes.REQUIRE_ACCOUNT])

    if not parameters.ok:
        return parameters.build()

    description = None

    if 'description' in request.data:
        parameters = handle_request.has_parameters([StringTypes.FORM_DESCRIPTION])

        if not parameters.ok:
            return parameters.build()
        
        description = request.data['description']

    form = models.Form.objects.create(
        user_id=response.user.id,
        title=request.data['title'],
        description=description,
        require_account=request.data['require_account'],
        creation_timestamp=time.time(),
        last_edit_timestamp=time.time()
    )

    response.data = form.to_dict()

    return response.build()


@api_view(('UPDATE', ))
def update_form(request):
    handle_request = HandleRequest(request)
    response = handle_request.is_authenticated()

    if not response.ok:
        return response.build()

    parameters = handle_request.has_parameters([CredentialTypes.FORM_ID])

    if not parameters.ok:
        return parameters.build()
    
    user = response.user
    form = models.Form.objects.filter(id=request.data['form_id'], user_id=user.id)

    if not form.exists():
        response.add_errors('form_id', ["You don't have edit permissions on this form."])
        response.status = status.HTTP_401_UNAUTHORIZED

        return response.build()
    
    edited = False

    form = form.first()
    
    if 'title' in request.data:
        parameters = handle_request.has_parameters([StringTypes.FORM_TITLE])

        if not parameters.ok:
            return parameters.build()
        
        form.title = request.data['title'] # type: ignore

        edited = True

    if 'description' in request.data:
        parameters = handle_request.has_parameters([StringTypes.FORM_DESCRIPTION])

        if not parameters.ok:
            return parameters.build()
        
        form.description = request.data['description'] # type: ignore

        edited = True

    if edited:
        form.last_edit_timestamp = time.time() # type: ignore
        form.save() # type: ignore

        response.data = form.to_dict() # type: ignore

        return response.build()

    response.add_errors('body', ["No editable fields provided. (title, description)"])
    response.status = status.HTTP_400_BAD_REQUEST

    return response.build()

@api_view(('POST', ))
def create_question(request):
    handle_request = HandleRequest(request)
    response = handle_request.is_authenticated()

    if not response.ok:
        return response.build()

    parameters = handle_request.has_parameters([CredentialTypes.FORM_ID, DefaultTypes.QUESTION_TYPE, StringTypes.QUESTION, StringTypes.QUESTION])

    if not parameters.ok:
        return parameters.build()
    
    user = response.user
    form = models.Form.objects.filter(id=request.data['form_id'], user_id=user.id)

    if not form.exists():
        response.add_errors('form_id', ["You don't have edit permissions on this form."])
        response.status = status.HTTP_401_UNAUTHORIZED

        return response.build()
    
    form = form.first()

    question_type = request.data['question_type']

    form.last_edit_timestamp = time.time() # type: ignore
    form.question_count += 1 # type: ignore
    form.save() # type: ignore

    if question_type == 3:
        question = models.Question.objects.create(
            form_id=form.id, # type: ignore
            user_id=user.id,
            index=form.question_count, # type: ignore
            question_type=question_type,
            question=request.data['question'],
            integer_answer=request.data['answer']
        )
    else:
        question = models.Question.objects.create(
            form_id=form.id, # type: ignore
            user_id=user.id,
            index=form.question_count, # type: ignore
            question_type=question_type,
            question=request.data['question'],
            string_answer=request.data['answer']
        )

    response.data = question.to_dict()
    
    return response.build()


@api_view(('UPDATE', ))
def update_question(request):
    handle_request = HandleRequest(request)
    response = handle_request.is_authenticated()

    if not response.ok:
        return response.build()

    parameters = handle_request.has_parameters([CredentialTypes.QUESTION_ID, DefaultTypes.INDEX])

    if not parameters.ok:
        return parameters.build()
    
    user = response.user
    question = models.Question.objects.filter(id=request.data['question_id'], user_id=user.id)

    if not question.exists():
        response.add_errors('form_id', ["You don't have edit permissions on this question."])
        response.status = status.HTTP_401_UNAUTHORIZED

        return response.build()
    
    question_1 = question.first()
    
    question = models.Question.objects.filter(form_id=question_1.form_id, index=request.data['index']) # type: ignore

    if not question.exists():
        response.add_errors('form_id', ["You cannot set the index to one that is invalid."])
        response.status = status.HTTP_401_UNAUTHORIZED

        return response.build()
    
    question_2 = question.first()

    question_2.index = question_1.index # type: ignore
    question_1.index = request.data['index'] # type: ignore

    question_1.save() # type: ignore
    question_2.save() # type: ignore

    response.data = question_1.to_dict() # type: ignore
    
    return response.build()