from django.db import models
from django.conf import settings
import random

class Category(models.Model):
    """Categories like Country, Animal, Food, etc."""
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Round(models.Model):
    """A game round with a specific letter."""
    letter = models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    @staticmethod
    def generate_letter():
        return random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

class Player(models.Model):
    """Players of the game."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

    @property
    def profile_picture_url(self):
        """Return Cloudinary URL or default static avatar"""
        if self.user.avatar:
            return self.user.avatar  # Cloudinary URL is stored as a string
        return settings.STATIC_URL + 'default-avatar.png'
    
class Submission(models.Model):
    """Player submissions for each round."""
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    is_valid = models.BooleanField(default=True)
    validation_message = models.CharField(max_length=255, blank=True)
    score_calculated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.player} - {self.category}: {self.word}"

class ValidAnswer(models.Model):
    """Valid words for each category."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)

    class Meta:
        unique_together = ('category', 'word')  # Prevent duplicates

    def __str__(self):
        return f"{self.word} ({self.category.name})"
