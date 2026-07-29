from django.urls import path
from .views import (
    BookDetailView, BookListView,
    BookCreateView, BookUpdateView, 
    BookDeleteView,ReviewDetailView, 
    ReviewListView, ReviewCreateView, 
    ReviewDeleteView, AuthorDetailView, 
    AuthorListView, GenreListView, 
    GenreDetailView, ReadingListUpdateView,
    ReadingListAddView, MyReadingListView,
    ReadingListDeleteView, FavoriteAddView,
    FavoriteDeleteView, FavoriteListView,
)

urlpatterns=[
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/add/', BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('books/<int:pk>/reviews/modify/', ReviewCreateView.as_view(), name='review_create'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),

    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),

    path('genres/', GenreListView.as_view(), name='genre_list'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre_detail'),

    path('books/<int:pk>/reading-list/', ReadingListUpdateView.as_view(), name='reading_list_update'),
    path('books/<int:pk>/reading-list/add/', ReadingListAddView.as_view(), name='reading_list_add'),
    path('books/<int:pk>/reading-list/delete/', ReadingListDeleteView.as_view(), name='reading_list_delete'),

    path('books/<int:pk>/favorites/add/', FavoriteAddView.as_view(), name='favorite_add'),
    path('books/<int:pk>/favorites/delete/', FavoriteDeleteView.as_view(), name='favorite_delete'),
    path('favorites/', FavoriteListView.as_view(), name='favorite_list'),

    path('my-reading-list/', MyReadingListView.as_view(), name='my_reading_list'),

]