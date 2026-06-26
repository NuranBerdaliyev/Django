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
    paginate_by=10
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

        params = self.request.GET.copy()
        params.pop('page', None)
        context['query_params'] = params.urlencode()

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
    
    
class ReviewCreateView(LoginRequiredMixin, View):
    template_name = 'book_app/review_form.html'

    def get_book(self):
        return get_object_or_404(Book, pk=self.kwargs['pk'])

    def get(self, request, pk):
        book = self.get_book()

        review = Review.objects.filter(
            added_by=request.user,
            book=book
        ).first()

        rating = Rating.objects.filter(
            added_by=request.user,
            book=book
        ).first()

        review_form = ReviewForm(instance=review)
        rating_form = RatingForm(instance=rating)

        return render(
            request,
            self.template_name,
            {
                'review_form': review_form,
                'rating_form': rating_form,
                'book': book,
            }
        )

    def post(self, request, pk):
        book = self.get_book()

        review_form = ReviewForm(request.POST)
        rating_form = RatingForm(request.POST)

        if review_form.is_valid() and rating_form.is_valid():
            with transaction.atomic():
                Review.objects.update_or_create(
                    added_by=request.user,
                    book=book,
                    defaults={
                        'text': review_form.cleaned_data['text']
                    }
                )

                Rating.objects.update_or_create(
                    added_by=request.user,
                    book=book,
                    defaults={
                        'value': rating_form.cleaned_data['value']
                    }
                )

            return redirect('book_detail', pk=book.pk)

        return render(
            request,
            self.template_name,
            {
                'review_form': review_form,
                'rating_form': rating_form,
                'book': book,
            }
        )
    
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