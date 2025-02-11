from django.core.files.storage import default_storage
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import os
from cloudinary.models import CloudinaryField

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
    avatar = CloudinaryField('image')

    def __str__(self):
        return self.username

    def delete_old_avatar(self):
        """Delete old avatar before saving a new one."""
        if self.pk and self.avatar:  # Ensure user exists and has an avatar
            try:
                old_instance = User.objects.get(pk=self.pk)
                if old_instance.avatar and old_instance.avatar.name != self.avatar.name:
                    # Check if file exists before deleting
                    if default_storage.exists(old_instance.avatar.name):
                        default_storage.delete(old_instance.avatar.name)
            except User.DoesNotExist:
                pass

    def save(self, *args, **kwargs):
        """Override save method to remove old avatar before saving the new one."""
        self.delete_old_avatar()
        super().save(*args, **kwargs)
