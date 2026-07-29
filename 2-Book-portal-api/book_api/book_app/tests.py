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
            reverse('api_author_detail_update_destroy', kwargs={'pk': self.author_one.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['fullname'], 'George Orwell')
        self.assertEqual(len(response.data['books']), 2)

    def test_genre_detail_returns_genre_books(self):
        response = self.client.get(
            reverse('api_genre_detail_update_destroy', kwargs={'pk': self.genre_scifi.pk})
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

class BookAndReviewCRUDAPITestCase(APITestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(
            username='user_a',
            password='testpassword123',
        )

        self.user_b = User.objects.create_user(
            username='user_b',
            password='testpassword123',
        )

        self.author = Author.objects.create(
            fullname='J. R. R. Tolkien',
            biography='English writer.',
        )

        self.genre = Genre.objects.create(
            name='Fantasy',
        )

        self.book_a = Book.objects.create(
            added_by=self.user_a,
            title='The Hobbit',
            description='A fantasy adventure.',
            published_year=1937,
            author=self.author,
        )
        self.book_a.genres.add(self.genre)

        self.book_b = Book.objects.create(
            added_by=self.user_b,
            title='The Lord of the Rings',
            description='An epic fantasy novel.',
            published_year=1954,
            author=self.author,
        )
        self.book_b.genres.add(self.genre)

        self.review_a = Review.objects.create(
            added_by=self.user_a,
            book=self.book_a,
            text='A great book.',
        )

        self.review_b = Review.objects.create(
            added_by=self.user_b,
            book=self.book_b,
            text='A classic fantasy story.',
        )

    def test_guest_cannot_create_book(self):
        response = self.client.post(
            reverse('api_book_list_create'),
            {
                'title': 'Dune',
                'description': 'Science-fiction novel.',
                'published_year': 1965,
                'author': self.author.pk,
                'genres': [self.genre.pk],
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_can_create_book(self):
        self.client.force_authenticate(user=self.user_a)

        response = self.client.post(
            reverse('api_book_list_create'),
            {
                'title': 'Dune',
                'description': 'Science-fiction novel.',
                'published_year': 1965,
                'author': self.author.pk,
                'genres': [self.genre.pk],
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_book = Book.objects.get(title='Dune')

        self.assertEqual(created_book.added_by, self.user_a)
        self.assertEqual(created_book.author, self.author)
        self.assertEqual(created_book.published_year, 1965)
        self.assertIn(self.genre, created_book.genres.all())

    def test_book_owner_can_patch_own_book(self):
        self.client.force_authenticate(user=self.user_a)

        response = self.client.patch(
            reverse(
                'api_book_detail_update_destroy',
                kwargs={'pk': self.book_a.pk},
            ),
            {
                'title': 'The Hobbit: Updated Edition',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book_a.refresh_from_db()

        self.assertEqual(
            self.book_a.title,
            'The Hobbit: Updated Edition',
        )

    def test_other_user_cannot_patch_book(self):
        self.client.force_authenticate(user=self.user_b)

        response = self.client.patch(
            reverse(
                'api_book_detail_update_destroy',
                kwargs={'pk': self.book_a.pk},
            ),
            {
                'title': 'Stolen Book Title',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.book_a.refresh_from_db()

        self.assertEqual(self.book_a.title, 'The Hobbit')

    def test_book_owner_can_delete_own_book(self):
        self.client.force_authenticate(user=self.user_a)

        response = self.client.delete(
            reverse(
                'api_book_detail_update_destroy',
                kwargs={'pk': self.book_a.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Book.objects.filter(pk=self.book_a.pk).exists()
        )

    def test_other_user_cannot_delete_book(self):
        self.client.force_authenticate(user=self.user_b)

        response = self.client.delete(
            reverse(
                'api_book_detail_update_destroy',
                kwargs={'pk': self.book_a.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertTrue(
            Book.objects.filter(pk=self.book_a.pk).exists()
        )

    def test_guest_cannot_create_review(self):
        response = self.client.post(
            reverse('api_reviews_list_create'),
            {
                'book': self.book_b.pk,
                'text': 'Guest review.',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_can_create_review(self):
        self.client.force_authenticate(user=self.user_a)

        response = self.client.post(
            reverse('api_reviews_list_create'),
            {
                'book': self.book_b.pk,
                'text': 'A detailed review by user A.',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_review = Review.objects.get(
            added_by=self.user_a,
            book=self.book_b,
        )

        self.assertEqual(
            created_review.text,
            'A detailed review by user A.',
        )

    def test_review_owner_can_patch_own_review(self):
        self.client.force_authenticate(user=self.user_a)

        response = self.client.patch(
            reverse(
                'api_reviews_detail_update_destroy',
                kwargs={'pk': self.review_a.pk},
            ),
            {
                'text': 'Updated review text.',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.review_a.refresh_from_db()

        self.assertEqual(
            self.review_a.text,
            'Updated review text.',
        )

    def test_other_user_cannot_patch_review(self):
        self.client.force_authenticate(user=self.user_b)

        response = self.client.patch(
            reverse(
                'api_reviews_detail_update_destroy',
                kwargs={'pk': self.review_a.pk},
            ),
            {
                'text': 'Attempted edit by another user.',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.review_a.refresh_from_db()

        self.assertEqual(
            self.review_a.text,
            'A great book.',
        )

    def test_review_owner_can_delete_own_review(self):
        self.client.force_authenticate(user=self.user_a)

        response = self.client.delete(
            reverse(
                'api_reviews_detail_update_destroy',
                kwargs={'pk': self.review_a.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Review.objects.filter(pk=self.review_a.pk).exists()
        )

    def test_other_user_cannot_delete_review(self):
        self.client.force_authenticate(user=self.user_b)

        response = self.client.delete(
            reverse(
                'api_reviews_detail_update_destroy',
                kwargs={'pk': self.review_a.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertTrue(
            Review.objects.filter(pk=self.review_a.pk).exists()
        )

class RatingAPITestCase(APITestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(
            username='user_a',
            password='testpassword123',
        )

        self.user_b = User.objects.create_user(
            username='user_b',
            password='testpassword123',
        )

        self.author = Author.objects.create(
            fullname='Frank Herbert',
            biography='American science-fiction writer.',
        )

        self.book = Book.objects.create(
            added_by=self.user_a,
            title='Dune',
            description='Science-fiction novel.',
            published_year=1965,
            author=self.author,
        )

    def test_guest_cannot_rate_book(self):
        response = self.client.put(
            reverse(
                'api_book_rating',
                kwargs={'pk': self.book.pk},
            ),
            {
                'value': 5,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertFalse(
            Rating.objects.filter(
                book=self.book,
            ).exists()
        )

    def test_authenticated_user_can_create_rating(self):
        self.client.force_authenticate(
            user=self.user_a,
        )

        response = self.client.put(
            reverse(
                'api_book_rating',
                kwargs={'pk': self.book.pk},
            ),
            {
                'value': 4,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        rating = Rating.objects.get(
            added_by=self.user_a,
            book=self.book,
        )

        self.assertEqual(
            rating.value,
            4,
        )

        self.assertEqual(
            response.data['book'],
            self.book.pk,
        )

        self.assertEqual(
            response.data['value'],
            4,
        )

    def test_put_updates_existing_rating_instead_of_creating_second_one(self):
        Rating.objects.create(
            added_by=self.user_a,
            book=self.book,
            value=2,
        )

        self.client.force_authenticate(
            user=self.user_a,
        )

        response = self.client.put(
            reverse(
                'api_book_rating',
                kwargs={'pk': self.book.pk},
            ),
            {
                'value': 5,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            Rating.objects.filter(
                added_by=self.user_a,
                book=self.book,
            ).count(),
            1,
        )

        rating = Rating.objects.get(
            added_by=self.user_a,
            book=self.book,
        )

        self.assertEqual(
            rating.value,
            5,
        )

    def test_different_users_can_rate_same_book(self):
        Rating.objects.create(
            added_by=self.user_a,
            book=self.book,
            value=4,
        )

        self.client.force_authenticate(
            user=self.user_b,
        )

        response = self.client.put(
            reverse(
                'api_book_rating',
                kwargs={'pk': self.book.pk},
            ),
            {
                'value': 5,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Rating.objects.filter(
                book=self.book,
            ).count(),
            2,
        )

    def test_user_can_delete_own_rating(self):
        Rating.objects.create(
            added_by=self.user_a,
            book=self.book,
            value=4,
        )

        self.client.force_authenticate(
            user=self.user_a,
        )

        response = self.client.delete(
            reverse(
                'api_book_rating',
                kwargs={'pk': self.book.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Rating.objects.filter(
                added_by=self.user_a,
                book=self.book,
            ).exists()
        )

    def test_user_cannot_delete_other_users_rating(self):
        Rating.objects.create(
            added_by=self.user_a,
            book=self.book,
            value=4,
        )

        self.client.force_authenticate(
            user=self.user_b,
        )

        response = self.client.delete(
            reverse(
                'api_book_rating',
                kwargs={'pk': self.book.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertTrue(
            Rating.objects.filter(
                added_by=self.user_a,
                book=self.book,
            ).exists()
        )

    def test_rating_changes_book_average_rating(self):
        Rating.objects.create(
            added_by=self.user_a,
            book=self.book,
            value=4,
        )

        self.client.force_authenticate(
            user=self.user_b,
        )

        self.client.put(
            reverse(
                'api_book_rating',
                kwargs={'pk': self.book.pk},
            ),
            {
                'value': 5,
            },
            format='json',
        )

        response = self.client.get(
            reverse(
                'api_book_detail_update_destroy',
                kwargs={'pk': self.book.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data['average_rating'],
            4.5,
        )

        self.assertEqual(
            response.data['ratings_count'],
            2,
        )