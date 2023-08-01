
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator


class UserProfile(AbstractUser):
    email = models.EmailField(validators=[EmailValidator(message="Invalid email format.")], unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.username
