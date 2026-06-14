from django.urls import path
from .views import (
    BookDetailView, BookListView,
    ReviewDetailView, ReviewListView,
    AuthorDetailView, AuthorListView,
    GenreListView, GenreDetailView,
)

urlpatterns=[
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('genres/', GenreListView.as_view(), name='genre_list'),
    path('genres/<int:pk>/', GenreListView.as_view(), name='genre_detail'),
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
]