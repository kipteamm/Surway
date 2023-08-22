from rest_framework.decorators import api_view
from rest_framework import status

from .request_handler import HandleRequest, CredentialTypes, DefaultTypes, StringTypes

from formapp import models


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

    form.question_count += 1 # type: ignore

    if question_type == 3:
        question = models.Question.objects.create(
            form_id=form.id, # type: ignore
            index=form.question_count, # type: ignore
            question_type=question_type,
            question=request.data['question'],
            integer_answer=request.data['answer']
        )
    else:
        question = models.Question.objects.create(
            form_id=form.id, # type: ignore
            index=form.question_count, # type: ignore
            question_type=question_type,
            question=request.data['question'],
            string_answer=request.data['answer']
        )

    response.data = question.to_dict()
    
    return response.build()