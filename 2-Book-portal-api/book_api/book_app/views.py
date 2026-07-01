from django.db.models import Avg, Count, Prefetch
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Author, Book, Genre, Review
from .serializers import (
    AuthorListSerializer,
    AuthorDetailSerializer,
    BookDetailSerializer,
    BookListSerializer,
    GenreListSerializer,
    GenreDetailSerializer,
    ReviewSerializer,
)
class AuthorListAPIView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer

class AuthorDetailAPIView(RetrieveAPIView):
    serializer_class = AuthorDetailSerializer

    def get_queryset(self):
        books_queryset = (
            Book.objects.select_related(
                'author',
            ).prefetch_related(
                'genres',
            )
            .annotate(
                average_rating=Avg('ratings__value'),
                ratings_count=Count('ratings'),
            )
            .order_by(
                '-created_at',
            )
        )

        return Author.objects.prefetch_related(
            Prefetch(
                'books',
                queryset=books_queryset,
            ),
        )

class GenreListAPIView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer

class GenreDetailAPIView(RetrieveAPIView):
    serializer_class = GenreDetailSerializer

    def get_queryset(self):
        books_queryset = (
            Book.objects.select_related(
                'author',
            )
            .prefetch_related(
                'genres',
            )
            .annotate(
                average_rating=Avg('ratings__value'),
                ratings_count=Count('ratings'),
            )
            .order_by(
                '-created_at',
            )
        )

        return Genre.objects.prefetch_related(
            Prefetch(
                'books',
                queryset=books_queryset,
            ),
        )

class BookListAPIView(ListAPIView):
    serializer_class = BookListSerializer

    def get_queryset(self):
        return (
            Book.objects.select_related(
                'author',
            )
            .prefetch_related(
                'genres',
            )
            .annotate(
                average_rating=Avg('ratings__value'),
                ratings_count=Count('ratings'),
            )
            .order_by(
                '-created_at',
            )
        )


class BookDetailAPIView(RetrieveAPIView):
    serializer_class = BookDetailSerializer

    def get_queryset(self):
        return (
            Book.objects.select_related(
                'author',
                'added_by',
            )
            .prefetch_related(
                'genres',
                Prefetch(
                    'reviews',
                    queryset=Review.objects.select_related(
                        'added_by',
                    ).order_by(
                        '-created_at',
                    ),
                ),
            )
            .annotate(
                average_rating=Avg('ratings__value'),
                ratings_count=Count('ratings'),
            )
        )


class ReviewListAPIView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.select_related(
            'book',
            'added_by',
        ).order_by(
            '-created_at',
        )


class ReviewDetailAPIView(RetrieveAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.select_related(
            'book',
            'added_by',
        )