import os
from django.core.management.base import BaseCommand
from game.models import ValidAnswer

class Command(BaseCommand):
    help = "Populate the ValidAnswer table with animals from a text file"

    def handle(self, *args, **kwargs):
        file_path = "data/animals.txt"  # Path to the text file
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                # Read the file and split by commas
                animals = file.read().strip().split(",")

                for animal in animals:
                    animal = animal.strip().capitalize()  # Standardize capitalization
                    self.add_valid_answer("Animal", animal)

            self.stdout.write(self.style.SUCCESS("Animals populated successfully."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading file: {e}"))

    def add_valid_answer(self, category, name):
        valid_answer, created = ValidAnswer.objects.get_or_create(
            category=category, word=name
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Added: {name}"))
        else:
            self.stdout.write(self.style.WARNING(f"Already exists: {name}"))
