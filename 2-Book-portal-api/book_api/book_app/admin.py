#book_app/admin.py
from django.contrib import admin
from .models import Author, Genre, Book, Review, Rating, ReadingList, Favorite

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(ReadingList)
admin.site.register(Favorite)