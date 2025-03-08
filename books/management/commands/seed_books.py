from django.core.management.base import BaseCommand
from faker import Faker
from books.models import Book, Category
from django.db import transaction
import random
import requests
import uuid
import os

from django.conf import settings
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = "Seeds the database with random books, categories, and downloads random images."

    def add_arguments(self, parser):
        parser.add_argument('--number', type=int, default=20,
                            help='How many books to create (default: 20)')

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker()
        number_of_books = options['number']

        self.stdout.write(self.style.WARNING(
            f"Seeding {number_of_books} books with random images (this may take a while)..."
        ))

        # 1) Ensure some categories
        category_names = ["Fiction", "Non-Fiction", "Science", "Biography",
                          "Children", "Fantasy", "Thriller", "Romance"]
        categories = []
        for cat_name in category_names:
            cat, created = Category.objects.get_or_create(name=cat_name)
            if created:
                cat.description = fake.paragraph(nb_sentences=2)
                cat.save()
            categories.append(cat)

        books_to_create = []
        for _ in range(number_of_books):
            books_to_create.append(Book(
                title=fake.sentence(nb_words=4),
                author=fake.name(),
                description=fake.paragraph(nb_sentences=5),
                category=random.choice(categories),
                is_premium=fake.boolean(chance_of_getting_true=50)
            ))

        # 2) Bulk create the Book objects *without* images first
        Book.objects.bulk_create(books_to_create)

        # 3) Now fetch them from the DB to attach images
        #    (We do this in a second step to get valid primary keys.)
        all_books = Book.objects.order_by('-id')[:number_of_books]
        image_count = 0

        for book in all_books:
            # Use a placeholder service like Picsum or placekitten, etc.
            # e.g. "https://picsum.photos/200/300" returns a random 200x300 image
            image_url = "https://picsum.photos/200/300"

            try:
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    # Create a unique filename
                    unique_filename = f"{uuid.uuid4()}.jpg"
                    # Save it to the Book model (locally in media/book_covers/)
                    book.image.save(unique_filename, ContentFile(response.content), save=True)
                    image_count += 1
                else:
                    self.stdout.write(self.style.WARNING(
                        f"Failed to download image for Book {book.pk}. Status code: {response.status_code}"
                    ))
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.WARNING(
                    f"Error downloading image for Book {book.pk}: {e}"
                ))

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded {number_of_books} books, with {image_count} images downloaded!"
        ))
