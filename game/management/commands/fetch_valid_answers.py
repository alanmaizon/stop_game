from django.core.management.base import BaseCommand
from game.models import ValidAnswer
from game.utils import fetch_countries  # Assume fetch_countries is in game/utils.py

class Command(BaseCommand):
    help = 'Fetch valid answers (e.g., countries) and populate the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching and inserting valid answers...")
        fetch_countries()
        self.stdout.write("Successfully fetched and inserted valid answers.")
