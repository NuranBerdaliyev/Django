from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import Author, Book, Review, Rating, ReadingList, Favorite
from django.urls import reverse
User=get_user_model()

class ReviewModelTest(TestCase):
    def test_user_cannot_review_same_book_twice(self):
        user=User.objects.create_user(
            username='test user',
            password='123456'
        )
        author=Author.objects.create(
            fullname='Test Author'
        )
        book=Book.objects.create(
            added_by=user,
            title='test book',
            author=author
        )
        Review.objects.create(
            added_by=user,
            book=book,
            text='test'
        )

        with self.assertRaises(IntegrityError):
            Review.objects.create(
                added_by=user,
                book=book,
                text='test'
            )

class BookModelTest(TestCase):
    def test_user_cannot_add_same_book_twice(self):
        user=User.objects.create_user(
            username='test user',
            password='123456'
        )

        author=Author.objects.create(
            fullname='Test Author'
        )

        Book.objects.create(
            added_by=user,
            title='test title',
            author=author
        )

        with self.assertRaises(IntegrityError):
            Book.objects.create(
                added_by=user,
                title='test title',
                author=author
            )

class RatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='rating_user',
            password='strong-password-123'
        )

        self.author = Author.objects.create(
            fullname='Test Author'
        )

        self.book = Book.objects.create(
            added_by=self.user,
            title='Test Book',
            author=self.author
        )

    def test_user_cannot_rate_same_book_twice(self):
        Rating.objects.create(
            added_by=self.user,
            book=self.book,
            value=5
        )

        with self.assertRaises(IntegrityError):
            Rating.objects.create(
                added_by=self.user,
                book=self.book,
                value=4
            )

class ReadingListModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='reading_user',
            password='strong-password-123'
        )

        self.author = Author.objects.create(
            fullname='Reading List Author'
        )

        self.book = Book.objects.create(
            added_by=self.user,
            title='Reading List Book',
            author=self.author
        )

    def test_user_cannot_add_same_book_to_reading_list_twice(self):
        ReadingList.objects.create(
            user=self.user,
            book=self.book,
            status=ReadingList.Status.WANT_TO_READ
        )

        with self.assertRaises(IntegrityError):
            ReadingList.objects.create(
                user=self.user,
                book=self.book,
                status=ReadingList.Status.READ
            )

    def test_reading_list_default_status_is_want_to_read(self):
        entry = ReadingList.objects.create(
            user=self.user,
            book=self.book
        )

        self.assertEqual(
            entry.status,
            ReadingList.Status.WANT_TO_READ
        )
class FavoriteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='favorite_user',
            password='strong-password-123'
        )

        self.author = Author.objects.create(
            fullname='Favorite Author'
        )

        self.book = Book.objects.create(
            added_by=self.user,
            title='Favorite Book',
            author=self.author
        )

    def test_user_cannot_add_same_book_to_favorites_twice(self):
        Favorite.objects.create(
            user=self.user,
            book=self.book
        )

        with self.assertRaises(IntegrityError):
            Favorite.objects.create(
                user=self.user,
                book=self.book
            )
class ObjectPermissionsTests(TestCase):
    def setUp(self):

        self.user_a = User.objects.create_user(
            username='user_a',
            password='strong-password-123'
        )

        self.user_b = User.objects.create_user(
            username='user_b',
            password='strong-password-123'
        )

        self.author = Author.objects.create(
            fullname='George Orwell',
            biography='English writer'
        )

        self.book = Book.objects.create(
            added_by=self.user_a,
            title='1984',
            description='Dystopian novel',
            published_year=1949,
            author=self.author,
        )

        self.review = Review.objects.create(
            added_by=self.user_a,
            book=self.book,
            text='A very strong review text.'
        )

        self.rating = Rating.objects.create(
            added_by=self.user_a,
            book=self.book,
            value=5
        )
    
    def test_guest_can_view_book_detail(self):
        url = reverse('book_detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_guest_is_redirected_to_login_when_trying_to_create_book(self):
        url=reverse('book_create')
        response=self.client.get(url)
        login_url=reverse('login')
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_guest_is_redirected_to_login_when_trying_to_update_book(self):
        url=reverse('book_update', kwargs={'pk': self.book.pk})
        response=self.client.get(url)
        login_url=reverse('login')
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_guest_is_redirected_to_login_when_trying_to_delete_book(self):
        url = reverse('book_delete', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_guest_is_redirected_to_login_when_trying_to_create_review(self):
        url = reverse('review_create', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_guest_is_redirected_to_login_when_trying_to_modify_review(self):
        url = reverse('review_create', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={url}')
    
    def test_guest_is_redirected_to_login_when_trying_to_delete_review(self):
        url = reverse('review_delete', kwargs={'pk': self.review.pk})
        response = self.client.get(url)
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={url}')
    
    def test_other_user_cannot_edit_someone_elses_book(self):
        self.client.force_login(self.user_b)
        url = reverse('book_update', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
    
    def test_other_user_cannot_delete_someone_elses_book(self):
        self.client.force_login(self.user_b)
        url = reverse('book_delete', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
    
    def test_other_user_cannot_delete_someone_elses_review(self):
        self.client.force_login(self.user_b)
        url = reverse('review_delete', kwargs={'pk': self.review.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_owner_can_edit_own_book(self):
        self.client.force_login(self.user_a)
        url = reverse('book_update', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_owner_can_delete_own_book(self):
        self.client.force_login(self.user_a)
        url = reverse('book_delete', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_owner_can_delete_own_review(self):
        self.client.force_login(self.user_a)
        url = reverse('review_delete', kwargs={'pk': self.review.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_other_user_can_view_book_detail(self):
        self.client.force_login(self.user_b)
        url = reverse('book_detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_update_someone_elses_book_with_post(self):
        self.client.force_login(self.user_b)
        url = reverse('book_update', kwargs={'pk': self.book.pk})
        response = self.client.post(url, {
            'title': 'Hacked title',
            'description': 'Changed by another user',
            'published_year': 2026,
            'author': self.author.pk,
        })
        self.assertEqual(response.status_code, 403)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, '1984')


    def test_other_user_cannot_delete_someone_elses_book_with_post(self):
        self.client.force_login(self.user_b)
        url = reverse('book_delete', kwargs={'pk': self.book.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Book.objects.filter(pk=self.book.pk).exists())

    def test_other_user_cannot_delete_someone_elses_review_with_post(self):
        self.client.force_login(self.user_b)
        url = reverse('review_delete', kwargs={'pk': self.review.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Review.objects.filter(pk=self.review.pk).exists())

    def test_owner_can_open_review_and_rating_form(self):
        self.client.force_login(self.user_a)
        url = reverse('review_create', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_owner_can_update_review_and_rating_together(self):
        self.client.force_login(self.user_a)
        url = reverse('review_create', kwargs={'pk': self.book.pk})
        response = self.client.post(url, {
            'text': 'Updated review text.',
            'value': 4,
        })
        self.assertRedirects(
            response,
            reverse('book_detail', kwargs={'pk': self.book.pk})
        )

        self.review.refresh_from_db()
        self.rating.refresh_from_db()

        self.assertEqual(self.review.text, 'Updated review text.')
        self.assertEqual(self.rating.value, 4)
    
    def test_other_user_creates_own_review_and_rating_without_changing_owner_data(self):
        self.client.force_login(self.user_b)
        url = reverse('review_create', kwargs={'pk': self.book.pk})
        response = self.client.post(url, {
            'text': 'Review from user B.',
            'value': 3,
        })
        self.assertRedirects(
            response,
            reverse('book_detail', kwargs={'pk': self.book.pk})
        )
        self.review.refresh_from_db()
        self.rating.refresh_from_db()
        self.assertEqual(self.review.text, 'A very strong review text.')
        self.assertEqual(self.rating.value, 5)
        user_b_review = Review.objects.get(
            added_by=self.user_b,
            book=self.book
        )
        user_b_rating = Rating.objects.get(
            added_by=self.user_b,
            book=self.book
        )
        self.assertEqual(user_b_review.text, 'Review from user B.')
        self.assertEqual(user_b_rating.value, 3)

    def test_owner_deleting_review_also_deletes_rating(self):
        self.client.force_login(self.user_a)
        url = reverse('review_delete', kwargs={'pk': self.review.pk})
        response = self.client.post(url)
        self.assertRedirects(
            response,
            reverse('book_detail', kwargs={'pk': self.book.pk})
        )
        self.assertFalse(
            Review.objects.filter(pk=self.review.pk).exists()
        )
        self.assertFalse(
            Rating.objects.filter(
                added_by=self.user_a,
                book=self.book
            ).exists()
        )
    
    def test_guest_is_redirected_to_login_when_trying_to_add_book_to_reading_list(self):
        url = reverse('reading_list_add', kwargs={'pk': self.book.pk})
        response = self.client.post(url)
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_user_can_add_book_to_reading_list(self):
        self.client.force_login(self.user_a)
        url = reverse('reading_list_add', kwargs={'pk': self.book.pk})
        response = self.client.post(url, {'next': reverse('book_detail', kwargs={'pk': self.book.pk})})
        self.assertRedirects(response, reverse('book_detail', kwargs={'pk': self.book.pk}))
        entry = ReadingList.objects.get(user=self.user_a, book=self.book)
        self.assertEqual(entry.status, ReadingList.Status.WANT_TO_READ)

    def test_user_can_change_reading_list_status(self):
        ReadingList.objects.create(user=self.user_a, book=self.book, status=ReadingList.Status.WANT_TO_READ)
        self.client.force_login(self.user_a)
        url = reverse('reading_list_update', kwargs={'pk': self.book.pk})
        response = self.client.post(url, {'status': ReadingList.Status.READ})
        self.assertRedirects(response, reverse('book_detail', kwargs={'pk': self.book.pk}))
        entry = ReadingList.objects.get(user=self.user_a, book=self.book)
        self.assertEqual(entry.status, ReadingList.Status.READ)
        self.assertEqual(ReadingList.objects.filter(user=self.user_a, book=self.book).count(), 1)

    def test_user_can_remove_book_from_reading_list(self):
        ReadingList.objects.create(user=self.user_a, book=self.book, status=ReadingList.Status.READING)
        self.client.force_login(self.user_a)
        url = reverse(
            'reading_list_delete',
            kwargs={'pk': self.book.pk}
        )
        response = self.client.post(url)
        self.assertRedirects(
            response,
            reverse('my_reading_list')
        )
        self.assertFalse(
            ReadingList.objects.filter(
                user=self.user_a,
                book=self.book
            ).exists()
        )


    def test_user_cannot_see_another_users_reading_list_entries(self):
        ReadingList.objects.create(
            user=self.user_a,
            book=self.book,
            status=ReadingList.Status.READ
        )

        self.client.force_login(self.user_b)

        response = self.client.get(
            reverse('my_reading_list')
        )

        self.assertEqual(response.status_code, 200)

        self.assertNotContains(
            response,
            self.book.title
        )


    def test_user_can_add_book_to_favorites(self):
        self.client.force_login(self.user_a)

        url = reverse(
            'favorite_add',
            kwargs={'pk': self.book.pk}
        )

        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse(
                'book_detail',
                kwargs={'pk': self.book.pk}
            )
        )

        self.assertTrue(
            Favorite.objects.filter(
                user=self.user_a,
                book=self.book
            ).exists()
        )


    def test_user_can_remove_book_from_favorites(self):
        Favorite.objects.create(
            user=self.user_a,
            book=self.book
        )

        self.client.force_login(self.user_a)

        url = reverse(
            'favorite_delete',
            kwargs={'pk': self.book.pk}
        )

        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse('favorite_list')
        )

        self.assertFalse(
            Favorite.objects.filter(
                user=self.user_a,
                book=self.book
            ).exists()
        )