from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Book


class Command(BaseCommand):
    help = 'Seeds database with sample books and superuser'

    def handle(self, *args, **kwargs):
        # Create admin user if not exists
        username = 'admin'
        password = 'adminpassword123'
        email = 'admin@example.com'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser created successfully: username='{username}', password='{password}'"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' already exists."))

        # Sample books
        sample_books = [
            {'title': 'Python Crash Course', 'author': 'Eric Matthes', 'category': 'Programming', 'price': 29.99, 'published_date': '2019-05-03'},
            {'title': 'Fluent Python', 'author': 'Luciano Ramalho', 'category': 'Programming', 'price': 49.99, 'published_date': '2022-03-31'},
            {'title': 'Python Cookbook', 'author': 'David Beazley', 'category': 'Programming', 'price': 39.99, 'published_date': '2013-05-10'},
            {'title': 'Clean Code', 'author': 'Robert C. Martin', 'category': 'Software Engineering', 'price': 34.95, 'published_date': '2008-08-01'},
            {'title': 'Design Patterns', 'author': 'Erich Gamma', 'category': 'Software Engineering', 'price': 54.99, 'published_date': '1994-10-21'},
            {'title': 'Learning Python', 'author': 'Mark Lutz', 'category': 'Programming', 'price': 59.99, 'published_date': '2013-06-12'},
            {'title': 'Python Tricks', 'author': 'Dan Bader', 'category': 'Programming', 'price': 24.99, 'published_date': '2017-10-25'},
            {'title': 'Automate the Boring Stuff with Python', 'author': 'Al Sweigart', 'category': 'Programming', 'price': 29.95, 'published_date': '2019-11-12'},
            {'title': 'Effective Python', 'author': 'Brett Slatkin', 'category': 'Programming', 'price': 44.99, 'published_date': '2019-11-15'},
            {'title': 'Building APIs with Django', 'author': 'William S. Vincent', 'category': 'Web Development', 'price': 38.00, 'published_date': '2021-04-10'},
        ]

        created_count = 0
        for book_data in sample_books:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded database ({created_count} new books added)."))
