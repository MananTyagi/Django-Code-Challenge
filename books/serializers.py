# serializers.py
from rest_framework import serializers
from .models import Book, Author, Bookshelf, Language, Subject, Format

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'birth_year', 'death_year']
        

class BookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookshelf
        fields = ['name']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['code']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']

class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ['mime_type', 'url']

class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
    bookshelves = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    formats = FormatSerializer(many=True)

    class Meta:
        model = Book
        fields = ['gutenberg_id','title', 'authors', 'bookshelves','languages', 'subjects', 'formats']

    def get_authors(self, obj):
        all_books_authors = obj.authors.all()
        author_instances = [book_author.author for book_author in all_books_authors]

        serializer = AuthorSerializer(author_instances, many=True)
        return serializer.data

    def get_bookshelves(self, obj):
        all_books_bookshelfs = obj.bookshelves.all()
        bookshelf_instances = [book_author.bookshelf for book_author in all_books_bookshelfs]

        serializer = BookshelfSerializer(bookshelf_instances, many=True)
        return serializer.data

    def get_languages(self, obj):
        all_books_languages = obj.languages.all()
        language_instances = [ book_language.language for book_language in all_books_languages]
        
        serializer = LanguageSerializer(language_instances, many=True)
        return serializer.data

    def get_subjects(self, obj):
        all_books_subject =  obj.subjects.all()
        subject_instances = [book_subject.subject for book_subject in all_books_subject]
        serializer = SubjectSerializer(subject_instances, many=True)
        return serializer.data

