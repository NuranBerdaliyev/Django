from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Author(models.Model):
    fullname=models.CharField(max_length=255)
    biography=models.TextField(blank=True)
    def __str__(self):
        return self.fullname

class Genre(models.Model):
    name=models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name
    
class Book(models.Model):
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='added_books'
    )
    title=models.CharField(max_length=255)
    description=models.TextField(blank=True)
    published_year=models.PositiveIntegerField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books'
    )
    genres=models.ManyToManyField(
        Genre, 
        related_name='books',
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['added_by', 'title', 'author'],
                name='unique_book_per_addedby_title_author'
            )
        ]

    def __str__(self):
        return self.title

class Review(models.Model):
    added_by=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='added_reviews'
    )
    book=models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['added_by', 'book'],
                name='unique_review_per_addedby_book'
            )
        ]
    def __str__(self):
        return f"{self.added_by} - review for {self.book}"

class Rating(models.Model):
    added_by=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    book=models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    value=models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['added_by', 'book'],
                name='unique_rating_per_addedby_book'
            )
        ]
    
    def __str__(self):
        return f"{self.added_by} rated {self.book}: {self.value}/5"
