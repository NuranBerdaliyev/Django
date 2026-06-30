#book_app/views.py
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Author, Book, Genre
from .serializers import (
    AuthorSerializer,
    BookDetailSerializer,
    BookListSerializer,
    GenreSerializer,
)

class AuthorListAPIView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailAPIView(RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class GenreListAPIView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDetailAPIView(RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class BookListAPIView(ListAPIView):
    serializer_class = BookListSerializer

    def get_queryset(self):
        return Book.objects.select_related(
            'author',
        ).prefetch_related(
            'genres',
        ).order_by(
            '-created_at',
        )

class BookDetailAPIView(RetrieveAPIView):
    serializer_class = BookDetailSerializer

    def get_queryset(self):
        return Book.objects.select_related(
            'author',
            'added_by',
        ).prefetch_related(
            'genres',
        )