from django.db import models

from utils.snowflakes import SnowflakeIDField, SnowflakeGenerator


class User(models.Model):
    # Identifiers
    id = SnowflakeIDField(primary_key=True, unique=True)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)

    token = models.CharField(max_length=255, null=True, blank=True)

    # Permissions
    permissions = models.IntegerField(default=1)

    # Settings
    theme = models.TextField(max_length=5000, default="dark")

    # Time records
    creation_timestamp = models.FloatField()

    def save(self, *args, **kwargs):
        if self.id == "unset":
            self.id = str(SnowflakeGenerator().generate_id())

        super().save(*args, **kwargs)

    def to_dict(self) -> dict:
        return {
            'user_id' : self.id,
            'email_address' : self.email_address,
            'theme' : self.theme,
            'creation_timestamp' : self.creation_timestamp
        }