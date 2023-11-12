from django.db.models.query import QuerySet

from rest_framework.response import Response
from rest_framework import status

from auth.models import User 

from typing import Optional, Union


class ResponseBuilder:
    def __init__(self) -> None:
        self._user: User
        self._data: Union[dict, list] = {}
        self._objects: QuerySet
        self._next_page: bool = False
        self._errors: list = []
        self._status: int = status.HTTP_200_OK
        self._origin: str

    def add_errors(self, field: str, errors: list) -> None:
        self._errors.append({
            'field' : field,
            'errors' : errors
        })

    @property
    def data(self) -> Union[dict, list]:
        return self._data

    @data.setter
    def data(self, data: Union[dict, list]):
        self._data = data

    @property
    def objects(self) -> QuerySet:
        return self._objects

    @objects.setter
    def objects(self, objects: QuerySet):
        self._objects = objects

    @property
    def next_page(self) -> bool:
        return self._next_page
    
    @next_page.setter
    def next_page(self, next_page: bool):
        self._next_page = next_page

    @property
    def user(self) -> User:
        return self._user
    
    @user.setter
    def user(self, user: User):
        self._user = user

    @property
    def status(self) -> Optional[int]:
        return self._status
    
    @status.setter
    def status(self, status: int):
        self._status = status

    @property
    def origin(self) -> str:
        return self._origin
    
    @origin.setter
    def origin(self, origin: str):
        self._origin = origin

    @property
    def ok(self) -> bool:
        if self._errors or self._status != status.HTTP_200_OK:
            return False
        
        return True
    
    def build(self) -> Response:
        if self._errors:
            return Response({'errors' : self._errors}, status=self._status)
        
        return Response(self._data, status=self._status)