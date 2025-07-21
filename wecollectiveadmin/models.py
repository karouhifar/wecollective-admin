from django.db import models
from django_cryptography.fields import encrypt


class SecureAdmin(models.Model):
    username = encrypt(models.CharField(max_length=150))
    password = encrypt(models.CharField(max_length=128))
    # other fields…
