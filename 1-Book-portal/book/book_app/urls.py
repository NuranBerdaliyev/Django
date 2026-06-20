from django.urls import path
from .views import (
    BookDetailView, BookListView,
    ReviewDetailView, ReviewListView,
    ReviewCreateView,
    AuthorDetailView, AuthorListView,
    GenreListView, GenreDetailView,
)

urlpatterns=[
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('genres/', GenreListView.as_view(), name='genre_list'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre_detail'),
    path('books/<int:pk>/reviews/add/', ReviewCreateView.as_view(), name='review_create')
]