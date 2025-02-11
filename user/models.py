from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Player', 'Player'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Player')

    # Static avatar choices
    AVATAR_CHOICES = [
        ('avatar1.gif', 'Avatar 1'),
        ('avatar2.gif', 'Avatar 2'),
        ('avatar3.gif', 'Avatar 3'),
    ]

    avatar = models.CharField(max_length=100, choices=AVATAR_CHOICES, default='avatar1.gif')

    def get_avatar_url(self):
        """Returns the static URL for the selected avatar"""
        return f"/static/images/avatars/{self.avatar}"

    def __str__(self):
        return self.username
