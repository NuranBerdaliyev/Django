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

class ReviewListSerializer(serializers.ModelSerializer):
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
    reviews=ReviewListSerializer(many=True, read_only=True)

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

class BookWriteSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'description',
            'published_year',
            'author',
            'genres',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
        ]

    def validate(self, attrs):
        request = self.context['request']

        title = attrs.get(
            'title',
            self.instance.title if self.instance else None,
        )
        author = attrs.get(
            'author',
            self.instance.author if self.instance else None,
        )

        books = Book.objects.filter(
            added_by=request.user,
            title=title,
            author=author,
        )

        if self.instance:
            books = books.exclude(pk=self.instance.pk)

        if books.exists():
            raise serializers.ValidationError(
                {
                    'non_field_errors': [
                        'You have already added this book.'
                    ]
                }
            )

        return attrs


class ReviewWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'book',
            'text',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
        ]

    def validate(self, attrs):
        request = self.context['request']

        book = attrs.get(
            'book',
            self.instance.book if self.instance else None,
        )

        reviews = Review.objects.filter(
            added_by=request.user,
            book=book,
        )

        if self.instance:
            reviews = reviews.exclude(pk=self.instance.pk)

        if reviews.exists():
            raise serializers.ValidationError(
                {
                    'non_field_errors': [
                        'You have already reviewed this book.'
                    ]
                }
            )

        return attrs
    
class AuthorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id',
            'fullname',
            'biography',
        ]
        read_only_fields = [
            'id',
        ]


class GenreWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'id',
            'name',
        ]
        read_only_fields = [
            'id',
        ]