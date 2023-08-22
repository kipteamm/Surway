from django.db import models

from .snowflakes import SnowflakeGenerator


class SnowflakeIDField(models.BigIntegerField):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = SnowflakeGenerator().generate_id
        kwargs['editable'] = False
        super().__init__(*args, **kwargs)


class User(models.Model):
    # Identifiers
    id = SnowflakeIDField(primary_key=True, unique=True)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)

    token = models.CharField(max_length=255, null=True, blank=True)

    # Permissions
    permissions = models.IntegerField(default=1)

    # Time records
    creation_timestamp = models.FloatField()

    def to_dict(self) -> dict:
        return {
            'user_id' : self.id,
            'email_address' : self.email_address,
            'creation_timestamp' : self.creation_timestamp
        }


class Form(models.Model):
    # Identifiers
    id = SnowflakeIDField(primary_key=True, unique=True)
    user_id = SnowflakeIDField()

    # Meta
    title = models.CharField(max_length=100, default="Untitled Form")
    description = models.TextField(max_length=1000, blank=True, null=True)
    question_count = models.IntegerField(default=0)

    # Settings
    require_login = models.BooleanField(default=False)
    require_email = models.BooleanField(default=False)

    # Time records
    creation_timestamp = models.FloatField()
    last_edit_timestamp = models.FloatField()

    def to_dict(self) -> dict:
        return {
            'form_id' : self.id,
            'user_id' : self.user_id,
            'title' : self.title,
            'description' : self.description,
            'question_count' : self.question_count,
            'require_login' : self.require_login,
            'require_email' : self.require_email,
            'creation_timestamp' : self.creation_timestamp,
            'last_edit_timestamp' : self.last_edit_timestamp
        }


class Question(models.Model):
    # Identifiers
    id = SnowflakeIDField(primary_key=True, unique=True)
    form_id = SnowflakeIDField()
    user_id = SnowflakeIDField()
    index = models.IntegerField()

    # Meta
    question_type = models.IntegerField()
    question = models.TextField(max_length=1000)
    string_answer = models.TextField(max_length=5000, blank=True, null=True)
    integer_answer = models.IntegerField(blank=True, null=True)

    def to_dict(self) -> dict:
        answer = self.string_answer
        
        if self.question_type == 3:
            answer = self.integer_answer

        return {
            'question_id' : self.id,
            'form_id' : self.form_id,
            'index' : self.index,
            'question_type' : self.question_type,
            'question' : self.question,
            'answer' : answer,
        }