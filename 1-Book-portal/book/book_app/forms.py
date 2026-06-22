from django.forms import ModelForm
from .models import Book, Review

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

