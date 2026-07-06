#book_app/urls.py
from django.urls import path
from .views import (
    AuthorDetailUpdateDestroyAPIView,
    AuthorListCreateAPIView,
    BookDetailUpdateDestroyAPIView,
    BookListCreateAPIView,
    GenreDetailUpdateDestroyAPIView,
    GenreListCreateAPIView,
    ReviewListCreateAPIView,
    ReviewDetailUpdateDestroyAPIView,
    BookRatingAPIView,
)

urlpatterns = [
    path('authors/', AuthorListCreateAPIView.as_view(), name='api_author_list_create'),
    path('authors/<int:pk>/', AuthorDetailUpdateDestroyAPIView.as_view(), name='api_author_detail_update_destroy'),

    path('genres/', GenreListCreateAPIView.as_view(), name='api_genre_list_create'),
    path('genres/<int:pk>/', GenreDetailUpdateDestroyAPIView.as_view(), name='api_genre_detail_update_destroy'),

    path('books/', BookListCreateAPIView.as_view(), name='api_book_list_create'),
    path('books/<int:pk>/', BookDetailUpdateDestroyAPIView.as_view(), name='api_book_detail_update_destroy'),

    path('reviews/', ReviewListCreateAPIView.as_view(), name='api_reviews_list_create'),
    path('reviews/<int:pk>/', ReviewDetailUpdateDestroyAPIView.as_view(), name='api_reviews_detail_update_destroy'),

    path('books/<int:pk>/rating/', BookRatingAPIView.as_view(), name='api_book_rating'),
]