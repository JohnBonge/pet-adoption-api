from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_shelter = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    

    # New fields
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    USERNAME_FIELD = 'email'  # this tells Django to use email for login
    REQUIRED_FIELDS = ['username']

    def mark_email_verified(self):
        self.is_email_verified = True
        self.email_verification_token = None
        self.save(update_fields=["is_email_verified", "email_verification_token"])