from django.views.generic import ListView, DetailView
from .models import Book, Author, Genre, Review

class BookListView(ListView):
    model=Book
    context_object_name='books'

    queryset=Book.objects.select_related(
        'author', 'added_by'
    ).prefetch_related('genres')

class BookDetailView(DetailView):
    model=Book
    queryset=Book.objects.select_related(
        'author', 'added_by'
    ).prefetch_related(
        'genres',
        'reviews'
    )

class AuthorListView(ListView):
    model=Author
    context_object_name='authors'
    
class AuthorDetailView(DetailView):
    model=Author
    queryset=Author.objects.prefetch_related('books')

class GenreListView(ListView):
    model=Genre
    context_object_name='genres'

class GenreDetailView(DetailView):
    model=Genre
    queryset=Genre.objects.prefetch_related('books')

class ReviewListView(ListView):
    model=Review
    context_object_name='reviews'
    queryset=Review.objects.select_related(
        'book', 'added_by'
    )

class ReviewDetailView(DetailView):
    model=Review
    queryset=Review.objects.select_related(
        'book', 'added_by'
    )
