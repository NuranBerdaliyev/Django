from django.views.generic import ListView, DetailView
from .models import Book, Author, Genre, Review

class BookListView(ListView):
    model=Book
    context_object_name='books'

    queryset=Book.objects.select_related(
        'author', 'added_by'
    ).prefetch_related('genres')
