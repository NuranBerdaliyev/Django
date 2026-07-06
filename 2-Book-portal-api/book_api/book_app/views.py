#book_app/views.py
from django.db.models import Avg, Count, Prefetch
from rest_framework import mixins
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Author, Book, Genre, Review
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    AuthorDetailSerializer,
    AuthorListSerializer,
    BookDetailSerializer,
    BookListSerializer,
    BookWriteSerializer,
    GenreDetailSerializer,
    GenreListSerializer,
    ReviewSerializer,
    ReviewWriteSerializer,
)


class AuthorListAPIView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer

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


class BookListCreateAPIView(ListCreateAPIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
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

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookWriteSerializer

        return BookListSerializer

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

    def perform_create(self, serializer):
        serializer.save(
            added_by=self.request.user,
        )


class BookDetailUpdateDestroyAPIView(RetrieveAPIView, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return BookWriteSerializer

        return BookDetailSerializer

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

    def patch(self, request, *args, **kwargs):
        return self.partial_update(
            request,
            *args,
            **kwargs,
        )

    def delete(self, request, *args, **kwargs):
        return self.destroy(
            request,
            *args,
            **kwargs,
        )


class ReviewListCreateAPIView(ListCreateAPIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    filterset_fields = [
        'book',
        'added_by__username',
    ]

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

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewWriteSerializer

        return ReviewSerializer

    def get_queryset(self):
        return Review.objects.select_related(
            'book',
            'added_by',
        )

    def perform_create(self, serializer):
        serializer.save(
            added_by=self.request.user,
        )


class ReviewDetailUpdateDestroyAPIView(
    RetrieveAPIView,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ReviewWriteSerializer

        return ReviewSerializer

    def get_queryset(self):
        return Review.objects.select_related(
            'book',
            'added_by',
        )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(
            request,
            *args,
            **kwargs,
        )

    def delete(self, request, *args, **kwargs):
        return self.destroy(
            request,
            *args,
            **kwargs,
        )