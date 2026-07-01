#book_app/serializers.py
from rest_framework import serializers
from .models import Author, Book, Genre, Review

class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id',
            'fullname',
            'biography',
        ]


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'id',
            'name',
        ]
class BookListSerializer(serializers.ModelSerializer):
    author = AuthorListSerializer(read_only=True)
    genres = GenreListSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(
        read_only=True,
        allow_null=True,
    )
    ratings_count = serializers.IntegerField(
        read_only=True,
    )
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'published_year',
            'author',
            'genres',
            'created_at',
            'average_rating',
            'ratings_count',
        ]

class AuthorDetailSerializer(serializers.ModelSerializer):
    books=BookListSerializer(many=True, read_only=True)
    class Meta:
        model=Author
        fields=[
            'id',
            'fullname',
            'biography',
            'books',
        ]
class GenreDetailSerializer(serializers.ModelSerializer):
    books=BookListSerializer(many=True, read_only=True)
    class Meta:
        model = Genre
        fields = [
            'id',
            'name',
            'books',
        ]

class ReviewSerializer(serializers.ModelSerializer):
    added_by = serializers.CharField(
        source='added_by.username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'book',
            'added_by',
            'text',
            'created_at',
        ]




class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorListSerializer(read_only=True)
    genres = GenreListSerializer(many=True, read_only=True)
    added_by = serializers.CharField(
        source='added_by.username',
        read_only=True,
    )
    average_rating = serializers.FloatField(
        read_only=True,
        allow_null=True,
    )
    ratings_count = serializers.IntegerField(
        read_only=True,
    )
    reviews=ReviewSerializer(many=True, read_only=True)

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
            'average_rating',
            'ratings_count',
            'reviews',
        ]