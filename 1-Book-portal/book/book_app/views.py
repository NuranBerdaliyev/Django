from django.views.generic import (
    ListView, DetailView,
    CreateView,    
)
from django.urls import reverse_lazy
from .models import Book, Author, Genre, Review
from .forms import BookForm, ReviewForm

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

class BookCreateView(CreateView):
    model=Book
    form_class=BookForm
    success_url=reverse_lazy('book_list')

    def form_valid(self, form):
        form.instance.added_by=self.request.user
        return super().form_valid(form)
    
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

class ReviewCreateView(CreateView):
    model=Review
    form_class=ReviewForm
    success_url=reverse_lazy('review_list')

    def form_valid(self, form):
        form.instance.added_by=self.request.user
        form.instance.book_id=self.kwargs['pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'book_detail', 
            kwargs={'pk': self.kwargs['pk']}
        )