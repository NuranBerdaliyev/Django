from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView,
    DeleteView, 
)
from django.urls import reverse_lazy
from .models import Book, Author, Genre, Review
from .forms import BookForm, ReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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
        'reviews__added_by'
    )

class BookCreateView(LoginRequiredMixin, CreateView):
    model=Book
    form_class=BookForm
    success_url=reverse_lazy('book_list')

    def form_valid(self, form):
        form.instance.added_by=self.request.user
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=Book
    form_class=BookForm
    def test_func(self):
        book=self.get_object()
        return book.added_by==self.request.user
    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})
    
    
class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Book
    success_url=reverse_lazy('book_list')
    def test_func(self):
        book=self.get_object()
        return book.added_by==self.request.user
    
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

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model=Review
    form_class=ReviewForm

    def form_valid(self, form):
        form.instance.added_by=self.request.user
        form.instance.book_id=self.kwargs['pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'book_detail', 
            kwargs={'pk': self.kwargs['pk']}
        )

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=Review
    form_class=ReviewForm

    def test_func(self):
        review=self.get_object()
        return review.added_by==self.request.user
    
    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.book.pk})
    
    
class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Review
    
    def test_func(self):
        review=self.get_object()
        return review.added_by==self.request.user
    
    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.book.pk})