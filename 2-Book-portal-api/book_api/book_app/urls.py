#book_app/urls.py
from django.urls import path
from .views import (
    AuthorDetailAPIView,
    AuthorListAPIView,
    BookDetailUpdateDestroyAPIView,
    BookListCreateAPIView,
    GenreDetailAPIView,
    GenreListAPIView,
    ReviewListCreateAPIView,
    ReviewDetailUpdateDestroyAPIView,
)

urlpatterns = [
    path('authors/', AuthorListAPIView.as_view(), name='api_author_list'),
    path('authors/<int:pk>/', AuthorDetailAPIView.as_view(), name='api_author_detail'),

    path('genres/', GenreListAPIView.as_view(), name='api_genre_list'),
    path('genres/<int:pk>/', GenreDetailAPIView.as_view(), name='api_genre_detail'),

    path('books/', BookListCreateAPIView.as_view(), name='api_book_list_create'),
    path('books/<int:pk>/', BookDetailUpdateDestroyAPIView.as_view(), name='api_book_detail_update_destroy'),

    path('reviews/', ReviewListCreateAPIView.as_view(), name='api_reviews_list_create'),
    path('reviews/<int:pk>/', ReviewDetailUpdateDestroyAPIView.as_view(), name='api_reviews_detail_update_destroy'),
]