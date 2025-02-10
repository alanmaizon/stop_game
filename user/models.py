import os
import boto3
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

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

    def delete_old_avatar(self):
        """Delete the previous avatar from S3 before updating."""
        if self.pk:  # Ensure the instance already exists in the database
            try:
                old_instance = User.objects.get(pk=self.pk)
                if old_instance.avatar and old_instance.avatar.name != self.avatar.name:
                    # Delete old file from AWS S3
                    s3 = boto3.client('s3',
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                    )
                    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                    s3.delete_object(Bucket=bucket_name, Key=old_instance.avatar.name)
            except User.DoesNotExist:
                pass  # If no old image exists, do nothing

    def save(self, *args, **kwargs):
        """Override save method to delete old avatar before saving new one."""
        self.delete_old_avatar()
        super().save(*args, **kwargs)
