from django.core.management.base import BaseCommand
from game.models import Game
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Populate the Game table with test games"

    def handle(self, *args, **kwargs):
        # Create test games
        for i in range(1, 6):  # Create 5 games
            start_time = datetime.now() - timedelta(days=i)
            end_time = start_time + timedelta(hours=1)
            
            game, created = Game.objects.get_or_create(
                start_time=start_time,
                end_time=end_time
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Game {game.id} created!"))
            else:
                self.stdout.write(self.style.WARNING(f"Game {game.id} already exists."))

        self.stdout.write(self.style.SUCCESS("Game population complete!"))
