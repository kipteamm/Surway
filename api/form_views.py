from django.core.cache import cache

from rest_framework.decorators import api_view
from rest_framework import status

from .request_handler import HandleRequest, CredentialTypes, DefaultTypes, StringTypes, ListTypes

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

    quiz = False

    if 'quiz' in request.data:
        parameters = handle_request.has_parameters([DefaultTypes.QUIZ])

        if not parameters.ok:
            return parameters.build()
        
        quiz = request.data['quiz']

    user = response.user

    form = models.Form.objects.create(
        user_id=user.id,
        title=request.data['title'],
        description=description,
        quiz=quiz,
        require_account=request.data['require_account'],
        creation_timestamp=time.time(),
        last_edit_timestamp=time.time()
    )

    cache.delete(f"total_storage:{user.id}")

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
    
    cache.delete(f"total_storage:{user.id}")

    response.add_errors('body', ["No editable fields provided. (title, description)"])
    response.status = status.HTTP_400_BAD_REQUEST

    return response.build()


@api_view(('DELETE', ))
def delete_form(request, form_id):
    handle_request = HandleRequest(request, [form_id])
    response = handle_request.is_authenticated()

    if not response.ok:
        return response.build()

    parameters = handle_request.has_parameters([CredentialTypes.FORM_ID])

    if not parameters.ok:
        return parameters.build()
    
    user = response.user
    form = models.Form.objects.filter(id=form_id, user_id=user.id)

    if not form.exists():
        response.add_errors('form_id', ["You don't have edit permissions on this form."])
        response.status = status.HTTP_401_UNAUTHORIZED

        return response.build()
    
    form.delete()

    cache.delete(f"total_storage:{user.id}")
    
    response.status = status.HTTP_204_NO_CONTENT
    
    return response.build()


@api_view(('POST', ))
def create_question(request):
    handle_request = HandleRequest(request)
    response = handle_request.is_authenticated()

    if not response.ok:
        return response.build()

    parameters = handle_request.has_parameters([CredentialTypes.FORM_ID, DefaultTypes.QUESTION_TYPE, StringTypes.QUESTION, DefaultTypes.REQUIRED])

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

    answer = request.data['answer']

    if not form.quiz: # type: ignore
        answer = None

    if question_type == 3:
        question = models.Question.objects.create(
            form_id=form.id, # type: ignore
            user_id=user.id,
            index=form.question_count, # type: ignore
            question_type=question_type,
            required=request.data['required'],
            question=request.data['question'],
            integer_answer=answer,
            creation_timestamp=time.time(),
            last_edit_timestamp=time.time()
        )
    else:
        question = models.Question.objects.create(
            form_id=form.id, # type: ignore
            user_id=user.id,
            index=form.question_count, # type: ignore
            question_type=question_type,
            required=request.data['required'],
            question=request.data['question'],
            string_answer=answer,
            creation_timestamp=time.time(),
            last_edit_timestamp=time.time()
        )

    cache.delete(f"total_storage:{user.id}")

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

    cache.delete(f"total_storage:{user.id}")
    
    return response.build()


@api_view(('POST', ))
def submit_answer(request):
    handle_request = HandleRequest(request)

    response = handle_request.has_parameters([CredentialTypes.FORM_ID, StringTypes.TRACK_ID, ListTypes.ANSWERS])

    if not response.ok:
        return response.build()
    
    form = models.Form.objects.get(id=request.data['form_id'])

    if form.require_account: # type: ignore
        response = handle_request.is_authenticated()

        if not response.ok:
            return response.build()
        
    if models.Answer.objects.filter(form_id=form.id, track_id=request.data['track_id']).exists():
        response.add_errors('track_id', ["You have already submitted an answer to this form."])
        response.status = status.HTTP_401_UNAUTHORIZED

        return response.build()
    
    for answer in request.data['answers']:
        question = models.Question.objects.filter(id=answer['question_id'], form_id=form.id)

        if not question.exists():
            response.add_errors('form_id', ["Invalid question provided."])
            response.status = status.HTTP_401_UNAUTHORIZED

            return response.build()
        
        question = question.first()

        answer = answer['answer']
        
        if question.question_type == 3: # type: ignore
            errors = DefaultTypes(answer).is_valid(DefaultTypes.INTEGER_ANSWER)

            if errors:
                response.add_errors(question.id, errors) # type: ignore
                response.status = status.HTTP_400_BAD_REQUEST

                return response.build()

            answer = models.Answer.objects.create(
                question_id=question.id, # type: ignore
                form_id=form.id,
                track_id=request.data['track_id'],
                integer_answer=answer,
                creation_timestamp=time.time()
            )

        else:
            errors = StringTypes(answer).is_valid(StringTypes.STRING_ANSWER)
            
            if errors:
                response.add_errors(question.id, errors) # type: ignore
                response.status = status.HTTP_400_BAD_REQUEST

                return response.build()

            answer = models.Answer.objects.create(
                question_id=question.id, # type: ignore
                form_id=form.id,
                track_id=request.data['track_id'],
                string_answer=answer,
                creation_timestamp=time.time()
            )

    response.status = status.HTTP_204_NO_CONTENT
    
    return response.build()


@api_view(('GET', ))
def get_answers(request, form_id, track_id):
    handle_request = HandleRequest(request, [form_id])
    parameters = handle_request.has_parameters([CredentialTypes.FORM_ID])

    if not parameters.ok:
        return parameters.build()

    response = handle_request.is_authenticated()

    user = response.user
    form = models.Form.objects.filter(id=form_id, user_id=user.id)

    if not form.exists():
        response.add_errors('form_id', ["You don't have edit permissions on this form."])
        response.status = status.HTTP_401_UNAUTHORIZED

        return response.build()

    form = form.first()

    answers = []

    for answer in models.Answer.objects.filter(form_id=form.id, track_id=track_id): # type: ignore
        answers.append(answer.to_dict(True))

    response.data = answers

    return response.build()