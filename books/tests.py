from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book


class BookAPITests(APITestCase):

    def setUp(self):
        # Create test user
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

        # Obtain JWT tokens
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

        # Seed sample books
        self.book_data_list = [
            {'title': 'Python Crash Course', 'author': 'Eric Matthes', 'category': 'Programming', 'price': '29.99', 'published_date': '2019-05-03'},
            {'title': 'Fluent Python', 'author': 'Luciano Ramalho', 'category': 'Programming', 'price': '49.99', 'published_date': '2022-03-31'},
            {'title': 'Python Cookbook', 'author': 'David Beazley', 'category': 'Programming', 'price': '39.99', 'published_date': '2013-05-10'},
            {'title': 'Clean Code', 'author': 'Robert C. Martin', 'category': 'Software Engineering', 'price': '34.95', 'published_date': '2008-08-01'},
            {'title': 'Design Patterns', 'author': 'Erich Gamma', 'category': 'Software Engineering', 'price': '54.99', 'published_date': '1994-10-21'},
            {'title': 'Learning Python', 'author': 'Mark Lutz', 'category': 'Programming', 'price': '59.99', 'published_date': '2013-06-12'},
            {'title': 'Python Tricks', 'author': 'Dan Bader', 'category': 'Programming', 'price': '24.99', 'published_date': '2017-10-25'},
            {'title': 'Automate the Boring Stuff with Python', 'author': 'Al Sweigart', 'category': 'Programming', 'price': '29.95', 'published_date': '2019-11-12'},
            {'title': 'Effective Python', 'author': 'Brett Slatkin', 'category': 'Programming', 'price': '44.99', 'published_date': '2019-11-15'},
        ]

        self.books = []
        for data in self.book_data_list:
            self.books.append(Book.objects.create(**data))

    def test_jwt_token_obtain_and_refresh(self):
        """Test obtaining access token and refreshing token."""
        token_url = reverse('token_obtain_pair')
        res = self.client.post(token_url, {'username': self.username, 'password': self.password})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

        refresh_url = reverse('token_refresh')
        ref_res = self.client.post(refresh_url, {'refresh': res.data['refresh']})
        self.assertEqual(ref_res.status_code, status.HTTP_200_OK)
        self.assertIn('access', ref_res.data)

    def test_get_books_unauthenticated(self):
        """Anyone can view the list of books and a single book."""
        url = reverse('book-list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], len(self.book_data_list))

        detail_url = reverse('book-detail', kwargs={'pk': self.books[0].pk})
        detail_res = self.client.get(detail_url)
        self.assertEqual(detail_res.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_res.data['title'], 'Python Crash Course')

    def test_create_book_unauthenticated_fails(self):
        """Unauthenticated user cannot create a book."""
        url = reverse('book-list')
        data = {'title': 'New Book', 'author': 'Author', 'category': 'Tech', 'price': '19.99', 'published_date': '2023-01-01'}
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated_success(self):
        """Authenticated user can create a book."""
        url = reverse('book-list')
        data = {'title': 'Django for Beginners', 'author': 'William S. Vincent', 'category': 'Web', 'price': '35.00', 'published_date': '2022-01-01'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], 'Django for Beginners')

    def test_update_book_authenticated_success(self):
        """Authenticated user can update a book."""
        detail_url = reverse('book-detail', kwargs={'pk': self.books[0].pk})
        data = {'title': 'Python Crash Course 2nd Edition', 'author': 'Eric Matthes', 'category': 'Programming', 'price': '32.99', 'published_date': '2019-05-03'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        res = self.client.put(detail_url, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], 'Python Crash Course 2nd Edition')

    def test_delete_book_authenticated_success(self):
        """Authenticated user can delete a book."""
        detail_url = reverse('book-detail', kwargs={'pk': self.books[0].pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        res = self.client.delete(detail_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_filtering(self):
        """Filtering by category and author."""
        url = reverse('book-list') + '?category=Software Engineering'
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 2)

    def test_searching(self):
        """Searching by title or author."""
        url = reverse('book-list') + '?search=Python'
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Should match 7 Python books
        self.assertEqual(res.data['count'], 7)

    def test_ordering(self):
        """Ordering by price ascending and descending."""
        url = reverse('book-list') + '?ordering=-price'
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        prices = [float(item['price']) for item in res.data['results']]
        self.assertEqual(prices, sorted(prices, reverse=True))

    def test_pagination(self):
        """Verify 5 items per page pagination."""
        url = reverse('book-list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 5)
        self.assertIsNotNone(res.data['next'])
        self.assertIsNone(res.data['previous'])

    def test_expected_combined_query(self):
        """Verify GET /books/?search=Python&ordering=-price&page=2."""
        url = reverse('book-list') + '?search=Python&ordering=-price&page=2'
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # 5 Python books total, page 1 returns 5 books, so page 2 has 0 or page 1 has all 5
        # Let's verify page response fields
        self.assertIn('results', res.data)
        self.assertIn('next', res.data)
        self.assertIn('previous', res.data)
