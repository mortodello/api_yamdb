import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (Categories, Comment, Genres,
                            Review, Title, GenresTitles)
from users_yamdb.models import YaMDBUser


class Command(BaseCommand):
    csv_files = {
        Categories: 'category.csv',
        Genres: 'genre.csv',
        GenresTitles: 'genre_title.csv',
        Title: 'titles.csv',
        Review: 'review.csv',
        Comment: 'comments.csv',
        YaMDBUser: 'users.csv',
    }

    def handle(self, *args, **options):
        for model, csv_file in self.csv_files.items():
            file_path = os.path.join(
                settings.BASE_DIR, 'static', 'data', csv_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                objects = [model(**row) for row in reader]
                model.objects.bulk_create(objects)

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены'))
