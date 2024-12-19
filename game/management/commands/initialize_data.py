from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Initialize database with test data for Games, Players, Rounds, and Valid Answers"

    def handle(self, *args, **kwargs):
        commands = [
            "populate_games",
            "populate_players",
            "populate_rounds",
            "populate_valid_answers",
        ]
        
        for cmd in commands:
            self.stdout.write(self.style.NOTICE(f"Running {cmd}..."))
            call_command(cmd)

        self.stdout.write(self.style.SUCCESS("Database initialization complete!"))
