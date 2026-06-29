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
    class Value(models.IntegerChoices):
        ONE=1, '1/5'
        TWO=2, '2/5'
        THREE=3, '3/5'
        FOUR=4, '4/5'
        FIVE=5, '5/5'
    added_by=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='added_ratings'
    )
    book=models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    value=models.PositiveIntegerField(
        choices=Value.choices,
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


class ReadingList(models.Model):
    class Status(models.TextChoices):
        WANT_TO_READ = 'want_to_read', 'Want to read'
        READING = 'reading', 'Reading'
        READ = 'read', 'Read'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='added_reading_list'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reading_list'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WANT_TO_READ
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                name='unique_book_in_user_reading_list'
            )
        ]

    def __str__(self):
        return f'{self.user} — {self.book} ({self.get_status_display()})'
    

class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='added_favorites'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                name='unique_book_in_user_favorites'
            )
        ]

    def __str__(self):
        return f'{self.user} — favorite: {self.book}'