from django.db.models import Avg, Count, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Author, Book, Genre, Review
from .serializers import (
    AuthorDetailSerializer,
    AuthorListSerializer,
    BookDetailSerializer,
    BookListSerializer,
    GenreDetailSerializer,
    GenreListSerializer,
    ReviewSerializer,
)


class AuthorListAPIView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        'fullname',
        'biography',
    ]

    ordering_fields = [
        'fullname',
    ]

    ordering = [
        'fullname',
    ]


class AuthorDetailAPIView(RetrieveAPIView):
    serializer_class = AuthorDetailSerializer

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

        return Author.objects.prefetch_related(
            Prefetch(
                'books',
                queryset=books_queryset,
            ),
        )


class GenreListAPIView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        'name',
    ]

    ordering_fields = [
        'name',
    ]

    ordering = [
        'name',
    ]


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

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        'author',
        'genres',
        'published_year',
    ]

    search_fields = [
        'title',
        'description',
        'author__fullname',
    ]

    ordering_fields = [
        'title',
        'published_year',
        'created_at',
        'average_rating',
        'ratings_count',
    ]

    ordering = [
        '-created_at',
    ]

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

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = {
        'book': [
            'exact',
        ],
        'added_by__username': [
            'exact',
        ],
    }

    search_fields = [
        'text',
        'book__title',
        'added_by__username',
    ]

    ordering_fields = [
        'created_at',
    ]

    ordering = [
        '-created_at',
    ]

    def get_queryset(self):
        return Review.objects.select_related(
            'book',
            'added_by',
        )


class ReviewDetailAPIView(RetrieveAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.select_related(
            'book',
            'added_by',
        )