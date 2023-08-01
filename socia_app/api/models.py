from enum import Enum

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator


class RequestStatus(Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class FriendRequestManager(models.Manager):
    def get_by_sender_receiver(self, sender, receiver):
        try:
            return self.get(sender=sender, receiver=receiver)
        except self.model.DoesNotExist:
            return None


class UserProfile(AbstractUser):
    email = models.EmailField(validators=[EmailValidator(message="Invalid email format.")], unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class FriendRequest(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=20, choices=[(status.value, status.name.title()) for status in RequestStatus],
                              default=RequestStatus.PENDING.value)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = FriendRequestManager()
