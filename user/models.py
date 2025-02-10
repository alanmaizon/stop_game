from django.contrib.auth.models import AbstractUser
from django.db import models

def user_avatar_upload_path(instance, filename):
    """Ensure avatars are stored as avatars/username.extension"""
    extension = filename.split('.')[-1]
    return f"avatars/{instance.username}.{extension}"

class User(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Player', 'Player'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Player')
    avatar = models.ImageField(upload_to=user_avatar_upload_path, blank=True, null=True)

    def __str__(self):
        return self.username
