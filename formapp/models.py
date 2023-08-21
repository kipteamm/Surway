from django.db import models

from snowflakes import SnowflakeGenerator


class SnowflakeIDField(models.BigIntegerField):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = SnowflakeGenerator().generate_id
        kwargs['editable'] = False
        super().__init__(*args, **kwargs)


class User(models.Model):
    # Identifiers
    id = SnowflakeIDField(primary_key=True)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    token = models.CharField(max_length=255)

    # Permissions
    permissions = models.IntegerField(default=1)

    # Time records
    creation_timestamp = models.FloatField()

    