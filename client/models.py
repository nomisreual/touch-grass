from django.db import models
from cryptography.fernet import Fernet
import os
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.ForeignKey(User, related_name="api_keys", on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=255, null=True, blank=True)
    encrypted_api_key = models.BinaryField(null=True, blank=True)

    @property
    def key(self) -> str:
        if not self.encrypted_api_key:
            return ""
        encryption_key = os.environ.get("ENCRYPTION_KEY")
        if not encryption_key:
            raise ValueError("ENCRYPTION_KEY environment variable is not set")
        cipher_suite = Fernet(encryption_key)
        return cipher_suite.decrypt(self.encrypted_api_key).decode()

    @key.setter
    def key(self, value) -> None:
        encryption_key = os.environ.get("ENCRYPTION_KEY")
        if not encryption_key:
            raise ValueError("ENCRYPTION_KEY environment variable is not set")
        cipher_suite = Fernet(encryption_key)
        self.encrypted_api_key = cipher_suite.encrypt(value.encode())

    def save(self, *args, **kwargs):
        # Additional logic before saving if needed
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.name}"