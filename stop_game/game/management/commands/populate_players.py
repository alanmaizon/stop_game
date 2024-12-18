from django.core.management.base import BaseCommand
from game.models import Player, Game

class Command(BaseCommand):
    help = "Populate the Player table with test players"

    def handle(self, *args, **kwargs):
        # Get all games
        games = Game.objects.all()

        for game in games:
            for i in range(1, 4):  # Add 3 players per game
                player_name = f"Player_{i}_Game_{game.id}"
                player, created = Player.objects.get_or_create(
                    game=game,
                    name=player_name
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"{player.name} added to Game {game.id}!"))
                else:
                    self.stdout.write(self.style.WARNING(f"{player.name} already exists."))

        self.stdout.write(self.style.SUCCESS("Player population complete!"))
