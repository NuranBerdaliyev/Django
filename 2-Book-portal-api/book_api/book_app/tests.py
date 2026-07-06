#book_app/tests.py
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Book, Genre, Rating, Review


User = get_user_model()


class ReadOnlyAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='nuran',
            password='testpassword123',
        )

        self.second_user = User.objects.create_user(
            username='other_user',
            password='testpassword123',
        )

        self.author_one = Author.objects.create(
            fullname='George Orwell',
            biography='English writer',
        )

        self.author_two = Author.objects.create(
            fullname='Frank Herbert',
            biography='American science-fiction writer',
        )

        self.genre_fiction = Genre.objects.create(name='Fiction')
        self.genre_scifi = Genre.objects.create(name='Science Fiction')

        self.book_one = Book.objects.create(
            added_by=self.user,
            title='Animal Farm',
            description='Political satire about a farm.',
            published_year=1945,
            author=self.author_one,
        )
        self.book_one.genres.add(self.genre_fiction)

        self.book_two = Book.objects.create(
            added_by=self.user,
            title='1984',
            description='Dystopian novel about totalitarianism.',
            published_year=1949,
            author=self.author_one,
        )
        self.book_two.genres.add(self.genre_fiction)

        self.book_three = Book.objects.create(
            added_by=self.second_user,
            title='Dune',
            description='Science-fiction novel set on Arrakis.',
            published_year=1965,
            author=self.author_two,
        )
        self.book_three.genres.add(self.genre_scifi)

        Rating.objects.create(
            added_by=self.user,
            book=self.book_one,
            value=4,
        )

        Rating.objects.create(
            added_by=self.second_user,
            book=self.book_one,
            value=5,
        )

        self.review = Review.objects.create(
            added_by=self.user,
            book=self.book_one,
            text='A strong political allegory.',
        )

    def test_book_list_returns_books(self):
        response = self.client.get(
            reverse('api_book_list_create')
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(len(response.data['results']), 3)

        first_book = response.data['results'][0]

        self.assertIn('id', first_book)
        self.assertIn('title', first_book)
        self.assertIn('author', first_book)
        self.assertIn('genres', first_book)
        self.assertIn('average_rating', first_book)
        self.assertIn('ratings_count', first_book)

    def test_book_detail_returns_full_information(self):
        response = self.client.get(
            reverse(
                'api_book_detail_update_destroy',
                kwargs={'pk': self.book_one.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Animal Farm')
        self.assertEqual(response.data['added_by'], self.user.username)
        self.assertEqual(response.data['average_rating'], 4.5)
        self.assertEqual(response.data['ratings_count'], 2)

        self.assertEqual(len(response.data['reviews']), 1)
        self.assertEqual(
            response.data['reviews'][0]['text'],
            'A strong political allegory.',
        )

    def test_book_list_searches_by_title(self):
        response = self.client.get(
            reverse('api_book_list_create'),
            {'search': 'Dune'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Dune')

    def test_book_list_searches_by_author_name(self):
        response = self.client.get(
            reverse('api_book_list_create'),
            {'search': 'Orwell'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_book_list_filters_by_author(self):
        response = self.client.get(
            reverse('api_book_list_create'),
            {'author': self.author_one.pk},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        for book in response.data['results']:
            self.assertEqual(book['author']['id'], self.author_one.pk)

    def test_book_list_filters_by_genre(self):
        response = self.client.get(
            reverse('api_book_list_create'),
            {'genres': self.genre_scifi.pk},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Dune')

    def test_book_list_filters_by_published_year(self):
        response = self.client.get(
            reverse('api_book_list_create'),
            {'published_year': 1949},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], '1984')

    def test_book_list_orders_by_published_year(self):
        response = self.client.get(
            reverse('api_book_list_create'),
            {'ordering': 'published_year'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        years = [
            book['published_year']
            for book in response.data['results']
        ]

        self.assertEqual(years, [1945, 1949, 1965])

    def test_author_detail_returns_author_books(self):
        response = self.client.get(
            reverse('api_author_detail', kwargs={'pk': self.author_one.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['fullname'], 'George Orwell')
        self.assertEqual(len(response.data['books']), 2)

    def test_genre_detail_returns_genre_books(self):
        response = self.client.get(
            reverse('api_genre_detail', kwargs={'pk': self.genre_scifi.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Science Fiction')
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books'][0]['title'], 'Dune')

    def test_review_list_filters_by_book(self):
        response = self.client.get(
            reverse('api_reviews_list_create'),
            {'book': self.book_one.pk},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['text'],
            'A strong political allegory.',
        )

    def test_review_detail_returns_review(self):
        response = self.client.get(
            reverse(
                'api_reviews_detail_update_destroy',
                kwargs={'pk': self.review.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['added_by'],
            self.user.username,
        )
        self.assertEqual(
            response.data['text'],
            'A strong political allegory.',
        )

    def test_book_detail_returns_404_for_unknown_book(self):
        response = self.client.get(
            reverse(
                'api_book_detail_update_destroy',
                kwargs={'pk': 99999},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pagination_returns_ten_books_per_page(self):
        for index in range(8):
            Book.objects.create(
                added_by=self.user,
                title=f'Extra Book {index}',
                description='Extra test book.',
                published_year=2000 + index,
                author=self.author_one,
            )

        response = self.client.get(
            reverse('api_book_list_create'),
            {'ordering': 'title'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 11)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])

        second_page_response = self.client.get(
            reverse('api_book_list_create'),
            {
                'ordering': 'title',
                'page': 2,
            },
        )

        self.assertEqual(
            second_page_response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            len(second_page_response.data['results']),
            1,
        )
        self.assertIsNone(second_page_response.data['next'])