from django.forms import ModelForm, Select
from .models import Book, Review, Rating, ReadingList

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
            'value': Select,
        }
    
class ReadingListForm(ModelForm):
    class Meta:
        model = ReadingList
        fields = [
            'status',
        ]
        widgets = {
            'status':Select,
        }