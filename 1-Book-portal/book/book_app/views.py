from django.views import View
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView,
    DeleteView, 
)
from django.db import transaction
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Avg, Count
from .models import Book, Author, Genre, Review, Rating
from .forms import BookForm, ReviewForm, RatingForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class BookListView(ListView):
    model=Book
    context_object_name='books'

    def get_queryset(self):
        books = Book.objects.select_related(
            'author', 'added_by'
        ).prefetch_related(
            'genres'
        ).annotate(
            average_rating=Avg('ratings__value')
        )

        query=self.request.GET.get('q')
        genre_id=self.request.GET.get('genre')
        ordering=self.request.GET.get('ordering')

        if query:
            books = books.filter(title__icontains=query)

        if genre_id:
            books = books.filter(genres__id=genre_id)

        if ordering == 'oldest':
            books = books.order_by('published_year')

        elif ordering == 'title':
            books = books.order_by('title')

        elif ordering == 'rating':
            books = books.order_by('-average_rating')

        else:
            books = books.order_by('-created_at')

        return books.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['genres'] = Genre.objects.all()
        context['selected_genre'] = self.request.GET.get('genre', '')
        context['selected_ordering'] = self.request.GET.get('ordering', '')
        context['search_query'] = self.request.GET.get('q', '')

        return context
    

class BookDetailView(DetailView):
    model=Book
    queryset=Book.objects.select_related(
        'author', 'added_by'
    ).prefetch_related(
        'genres',
        'reviews__added_by'
    ).annotate(
        average_rating=Avg('ratings__value'),
        ratings_count=Count('ratings')
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ratings_by_user = {
            rating.added_by_id: rating.value
            for rating in self.object.ratings.all()
        }

        reviews = self.object.reviews.all()

        for review in reviews:
            review.rating_value = ratings_by_user.get(review.added_by_id)

        context['reviews'] = reviews

        return context

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
    ).prefetch_related(
        'book__ratings'
    )

    def get_queryset(self):
        reviews = super().get_queryset()

        for review in reviews:
            review.rating_value = next(
                (
                    rating.value
                    for rating in review.book.ratings.all()
                    if rating.added_by_id == review.added_by_id
                ),
                None
            )

        return reviews

class ReviewDetailView(DetailView):
    model=Review
    queryset=Review.objects.select_related(
        'book', 'added_by'
    ).prefetch_related(
        'book__ratings'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['rating'] = self.object.book.ratings.filter(
            added_by=self.object.added_by
        ).first()

        return context
    
    
class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review

    def test_func(self):
        review = self.get_object()
        return review.added_by == self.request.user

    def form_valid(self, form):
        review = self.get_object()

        with transaction.atomic():
            Rating.objects.filter(
                added_by=review.added_by,
                book=review.book
            ).delete()

            review.delete()

        return redirect('book_detail', pk=review.book.pk)