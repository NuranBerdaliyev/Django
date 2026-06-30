#book_app/serializers.py
from rest_framework import serializers
from .models import Author, Book, Genre

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id',
            'fullname',
            'biography',
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'id',
            'name',
        ]


class BookListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'published_year',
            'author',
            'genres',
            'created_at',
        ]


class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    added_by = serializers.CharField(
        source='added_by.username',
        read_only=True,
    )

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'description',
            'published_year',
            'created_at',
            'added_by',
            'author',
            'genres',
        ]