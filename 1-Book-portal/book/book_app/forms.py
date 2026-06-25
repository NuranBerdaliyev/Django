from django.forms import ModelForm, Select
from .models import Book, Review, Rating

class BookForm(ModelForm):
    class Meta:
        model=Book
        fields=[
            'title',
            'description',
            'published_year',
            'author',
            'genres',
        ]
'''
class AuthorForm(ModelForm):
    class Meta:
        model=Author
        fields=[
            'fullname',
            'biography',
        ]

'''

class ReviewForm(ModelForm):
    class Meta:
        model=Review
        fields=[
            'text',
        ]
'''
class GenreForm(ModelForm):
    class Meta:
        model=Genre
        fields=[
            'name',
        ]
'''
class RatingForm(ModelForm):
    class Meta:
        model=Rating
        fields=[
            'value',
        ]
        widgets={
            'value': Select(
                choices=[
                    (1, '1/5'),
                    (2, '2/5'),
                    (3, '3/5'),
                    (4, '4/5'),
                    (5, '5/5'),
                ]
            )
        }