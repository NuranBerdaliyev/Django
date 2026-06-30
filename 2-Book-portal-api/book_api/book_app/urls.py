#book_app/urls.py
from django.urls import path
from .views import (
    AuthorDetailAPIView,
    AuthorListAPIView,
    BookDetailAPIView,
    BookListAPIView,
    GenreDetailAPIView,
    GenreListAPIView,
)

urlpatterns = [
    path('authors/', AuthorListAPIView.as_view(), name='api_author_list'),
    path('authors/<int:pk>/', AuthorDetailAPIView.as_view(), name='api_author_detail'),

    path('genres/', GenreListAPIView.as_view(), name='api_genre_list'),
    path('genres/<int:pk>/', GenreDetailAPIView.as_view(), name='api_genre_detail'),

    path('books/', BookListAPIView.as_view(), name='api_book_list'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='api_book_detail'),
]