from django.core.management.base import BaseCommand
from game.models import Round, Game
import random
import string

class Command(BaseCommand):
    help = "Populate the Round table with test rounds"

    def handle(self, *args, **kwargs):
        # Get all games
        games = Game.objects.all()

        for game in games:
            for i in range(1, 4):  # Add 3 rounds per game
                random_letter = random.choice(string.ascii_uppercase)
                round_obj, created = Round.objects.get_or_create(
                    game=game,
                    round_letter=random_letter
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Round {round_obj.id} with letter {random_letter} added to Game {game.id}!"))
                else:
                    self.stdout.write(self.style.WARNING(f"Round {round_obj.id} already exists."))

        self.stdout.write(self.style.SUCCESS("Round population complete!"))
