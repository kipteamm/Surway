from __future__ import annotations

from django.http import HttpRequest

from rest_framework import status

from authentication.models import User
from app.models import Form, Question, Answer

from utils import permissions
from utils import functions

from api import response_builder

from typing import Union, Optional

from dataclasses import dataclass

import json


@dataclass(frozen=True, order=True)
class _StringType:
    field_name: str
    data_type: type
    min_length: int
    max_length: int
    nullable: bool


class StringTypes:
    FORM_TITLE = _StringType('title', str, 1, 100, False)
    FORM_DESCRIPTION = _StringType('description', str, 0, 1000, True)

    QUESTION = _StringType('question', str, 1, 1000, False)

    TRACK_ID = _StringType('track_id', str, 0, 256, True)
    STRING_ANSWER = _StringType('answer', str, 1, 5000, False)

    def __init__(self, value: str) -> None:
        self.value = value
        self.parameter_errors = []

    def is_valid(self, parameter: _StringType, premium: int = 0) -> list:
        if self.value == None:
            if not parameter.nullable:
                self.parameter_errors.append('invalid type')

                return self.parameter_errors
            
            return []

        if type(self.value) != parameter.data_type:
            self.parameter_errors.append('invalid type')

            return self.parameter_errors

        if len(self.value) < parameter.min_length:
            self.parameter_errors.append(f'minimum length not reached by: {parameter.min_length - len(self.value)}')

        if len(self.value) > parameter.max_length:
            self.parameter_errors.append(f'maximum exceeded by: {len(self.value) - parameter.max_length}')

        return self.parameter_errors


@dataclass(frozen=True, order=True)
class _ListType:
    field_name: str
    data_type: type
    min_length: int
    max_length: Optional[int]


class ListTypes:
    ANSWERS = _ListType('answers', list, 1, None)

    def __init__(self, value: str) -> None:
        self.value = value
        self.parameter_errors = []

    def is_valid(self, parameter: _ListType, premium: int=0) -> list:
        if type(self.value) != parameter.data_type:
            self.parameter_errors.append('invalid type')

            return self.parameter_errors

        if len(self.value) < parameter.min_length:
            self.parameter_errors.append(f'minumum length not reached by: {parameter.min_length - len(self.value)}')

        if parameter.max_length:
            if len(self.value) > parameter.max_length:
                self.parameter_errors.append(f'maximum exceeded by: {len(self.value) - parameter.max_length}')

        return self.parameter_errors


@dataclass(frozen=True, order=True)
class _DefaultType:
    field_name: str
    data_type: type


class DefaultTypes:
    QUIZ = _DefaultType('quiz', bool)
    REQUIRE_ACCOUNT = _DefaultType('require_account', bool)

    INDEX = _DefaultType('index', int)
    QUESTION_TYPE = _DefaultType('question_type', int)
    REQUIRED = _DefaultType('required', bool)

    STRING_ANSWER = _DefaultType('answer', str)
    INTEGER_ANSWER = _DefaultType('answer', int)

    def __init__(self, value: str) -> None:
        self.value = value
        self.parameter_errors = []

    def is_valid(self, parameter: _DefaultType):
        if type(self.value) != parameter.data_type:
            self.parameter_errors.append('invalid type')

        return self.parameter_errors


@dataclass(frozen=True, order=True)
class _CredentialType:
    field_name: str
    data_type: type


class CredentialTypes:
    USERNAME = _CredentialType('username', str)
    EMAIL_ADDRESS = _CredentialType('email_address', str)
    
    USER_ID = _CredentialType('user_id', str)
    FORM_ID = _CredentialType('form_id', str)
    QUESTION_ID = _CredentialType('question_id', str)

    def __init__(self, value: str) -> None:
        self.value = value
        self.parameter_errors = []

    def is_valid(self, parameter: _CredentialType) -> list:
        if type(self.value) != parameter.data_type:
            self.parameter_errors.append('invalid type')

            return self.parameter_errors

        match parameter:
            case self.USERNAME:
                if not User.objects.filter(username__iexact=self.value).exists() and self.value != "@me":
                    self.parameter_errors.append('no user found with that username')

            case self.EMAIL_ADDRESS:
                if not User.objects.filter(email_address__iexact=self.value).exists():
                    self.parameter_errors.append('no user found with that email address')

            case self.USER_ID:
                if not User.objects.filter(id=self.value).exists():
                    self.parameter_errors.append('user not found')

            case self.FORM_ID:
                if not Form.objects.filter(id=self.value).exists():
                    self.parameter_errors.append('form not found')

            case self.QUESTION_ID:
                if not Question.objects.filter(id=self.value).exists():
                    self.parameter_errors.append('question not found')

        return self.parameter_errors


class HandleRequest:
    def __init__(self, request: HttpRequest, arguments: Optional[list]=None) -> None:
        self._request_meta = request.META
        self._request_data = request.data # type: ignore
        self._arguments = arguments
        self._permissions = 0
        self._origin = functions.sha256(request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0] if request.META.get('HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')) # type: ignore


    def is_authenticated(self, permission: int=1) -> response_builder.ResponseBuilder:
        response = response_builder.ResponseBuilder()
        response.origin = self._origin

        if not 'HTTP_AUTHORIZATION' in self._request_meta:
            response.add_errors('authentication', ['no token provided'])
            response.status = status.HTTP_401_UNAUTHORIZED

            return response

        if not User.objects.filter(token=self._request_meta['HTTP_AUTHORIZATION']).exists():
            response.add_errors('authentication', ['invalid token provided'])
            response.status = status.HTTP_401_UNAUTHORIZED

            return response

        user = User.objects.get(token=self._request_meta['HTTP_AUTHORIZATION'])

        self._permissions = user.permissions

        if not permissions.Permissions(permissions=permission) in permissions.Permissions(permissions=self._permissions):
            response.add_errors('authentication', ['you are missing the right permissions'])
            response.status = status.HTTP_401_UNAUTHORIZED

            return response

        response.status = status.HTTP_200_OK
        response.user = user

        return response


    def has_parameters(self, parameters: list[Union[_StringType, _ListType, _DefaultType, _CredentialType]]) -> response_builder.ResponseBuilder:
        response = response_builder.ResponseBuilder()
        response.origin = self._origin

        for index, parameter in enumerate(parameters):

            if not self._arguments:
                if 'data' in self._request_data:
                    self._request_data = json.loads(self._request_data['data'])

                if not parameter.field_name in self._request_data:
                    response.add_errors(parameter.field_name, ['field not present in request'])
                    response.status = status.HTTP_400_BAD_REQUEST

                    continue

                parameter_value = self._request_data[parameter.field_name]
            else:
                parameter_value = self._arguments[index]

            if isinstance(parameter, _StringType):
                errors = StringTypes(parameter_value).is_valid(parameter, self._permissions)

                if errors:
                    response.add_errors(parameter.field_name, errors)
                    response.status = status.HTTP_400_BAD_REQUEST

                continue

            if isinstance(parameter, _ListType):
                errors = ListTypes(parameter_value).is_valid(parameter, self._permissions)

                if errors:
                    response.add_errors(parameter.field_name, errors)
                    response.status = status.HTTP_400_BAD_REQUEST

                continue

            if isinstance(parameter, _CredentialType):
                errors = CredentialTypes(parameter_value).is_valid(parameter)

                if errors:
                    response.add_errors(parameter.field_name, errors)
                    response.status = status.HTTP_400_BAD_REQUEST

                continue

        if response.status == status.HTTP_400_BAD_REQUEST:
            return response

        response.status = status.HTTP_200_OK

        return response