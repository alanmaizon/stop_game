import csv
from django.core.management.base import BaseCommand
from game.models import ValidAnswer

class Command(BaseCommand):
    help = "Populate the ValidAnswer table with cities and countries from a CSV file"

    def handle(self, *args, **kwargs):
        file_path = "data/worldcities.csv"  # Update with the actual path to your CSV
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Assuming the CSV has 'country' and 'city' columns
                    # self.add_valid_answer("Country", row["country"])
                    self.add_valid_answer("City", row["city_ascii"])
            self.stdout.write(self.style.SUCCESS("CSV data populated successfully."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading CSV file: {e}"))

    def add_valid_answer(self, category, name):
        valid_answer, created = ValidAnswer.objects.get_or_create(
            category=category, word=name
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Added: {name}"))
        else:
            self.stdout.write(self.style.WARNING(f"Already exists: {name}"))