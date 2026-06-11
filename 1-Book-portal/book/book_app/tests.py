from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import Author, Book, Review, Genre
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
