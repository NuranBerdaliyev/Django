from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import Author, Book, Review, Genre
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
            text='test',
            rating=5
        )

        with self.assertRaises(IntegrityError):
            Review.objects.create(
                added_by=user,
                book=book,
                text='test',
                rating=4
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
            rating=5,
            text='A very strong review text.'
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

    def test_guest_is_redirected_to_login_when_trying_to_edit_review(self):
        url = reverse('review_update', kwargs={'pk': self.review.pk})
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
    
    def test_other_user_cannot_edit_someone_elses_review(self):
        self.client.force_login(self.user_b)
        url = reverse('review_update', kwargs={'pk': self.review.pk})
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
    
    def test_owner_can_edit_own_review(self):
        self.client.force_login(self.user_a)
        url = reverse('review_update', kwargs={'pk': self.review.pk})
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


    def test_other_user_cannot_update_someone_elses_review_with_post(self):
        self.client.force_login(self.user_b)
        url = reverse('review_update', kwargs={'pk': self.review.pk})
        response = self.client.post(url, {
            'rating': 1,
            'text': 'Hacked review',
        })
        self.assertEqual(response.status_code, 403)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 5)


    def test_other_user_cannot_delete_someone_elses_review_with_post(self):
        self.client.force_login(self.user_b)
        url = reverse('review_delete', kwargs={'pk': self.review.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Review.objects.filter(pk=self.review.pk).exists())