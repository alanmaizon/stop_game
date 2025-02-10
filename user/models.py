from django.core.files.storage import default_storage
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
        """Elimina el avatar anterior antes de actualizarlo."""
        if self.pk:  # Asegura que el usuario ya existe en la BD
            try:
                old_instance = User.objects.get(pk=self.pk)
                if old_instance.avatar and old_instance.avatar.name != self.avatar.name:
                    default_storage.delete(old_instance.avatar.name)  # Usar django-storages
            except User.DoesNotExist:
                pass

    def save(self, *args, **kwargs):
        """Sobreescribe save para eliminar el avatar antiguo antes de guardar el nuevo."""
        self.delete_old_avatar()
        super().save(*args, **kwargs)