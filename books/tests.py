from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Author, Book, BookAuthors, BookBookshelves, BookLanguages, BookSubjects, Bookshelf, Format, Language, Subject

class BookListAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create more than the default pagination size (e.g., 25)
        for i in range(25):
            Book.objects.create(
                download_count=100+i+1,
                gutenberg_id=98324832+i+1,
                media_type=f'text{i+1}',
                title=f'Test Book{i+1}'
            )

    def test_pagination(self):
        url = reverse('book_query')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that 20 items per page are returned
        self.assertEqual(len(response.data['results']['books']), 20)
        # Check that pagination information is included in the response
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        
        
        
class ModelsTestCase(TestCase):
    def setUp(self):
        # Create some test data for the models
        self.author = Author.objects.create(name='Test Author', birth_year=1990, death_year=2020)
        self.book = Book.objects.create(download_count=100, gutenberg_id=123456, media_type='text', title='Test Book')
        self.bookshelf = Bookshelf.objects.create(name='Test Bookshelf')
        self.language = Language.objects.create(code='en')
        self.subject = Subject.objects.create(name='Test Subject')
        self.format = Format.objects.create(mime_type='text/plain', url='http://example.com/book', book=self.book)

    def test_author_creation(self):
        author = Author.objects.get(name='Test Author')
        self.assertEqual(author.birth_year, 1990)
        self.assertEqual(author.death_year, 2020)

    def test_book_creation(self):
        book = Book.objects.get(title='Test Book')
        self.assertEqual(book.download_count, 100)
        self.assertEqual(book.gutenberg_id, 123456)
        self.assertEqual(book.media_type, 'text')

    def test_bookshelf_creation(self):
        bookshelf = Bookshelf.objects.get(name='Test Bookshelf')
        self.assertEqual(bookshelf.name, 'Test Bookshelf')

    def test_language_creation(self):
        language = Language.objects.get(code='en')
        self.assertEqual(language.code, 'en')

    def test_subject_creation(self):
        subject = Subject.objects.get(name='Test Subject')
        self.assertEqual(subject.name, 'Test Subject')

    def test_format_creation(self):
        format = Format.objects.get(mime_type='text/plain')
        self.assertEqual(format.url, 'http://example.com/book')
        self.assertEqual(format.book.title, 'Test Book')
    
    def test_book_author_relation(self):
        book_author = BookAuthors.objects.create(book=self.book, author=self.author)
        self.assertEqual(book_author.book, self.book)
        self.assertEqual(book_author.author, self.author)

    # Similar tests for other models...

    def test_bookshelf_relation(self):
        book_bookshelf = BookBookshelves.objects.create(book=self.book, bookshelf=self.bookshelf)
        self.assertEqual(book_bookshelf.book, self.book)
        self.assertEqual(book_bookshelf.bookshelf, self.bookshelf)
        
    def test_book_language_relation(self):
        # Create a BookLanguages instance linking the book and language
        book_language = BookLanguages.objects.create(book=self.book, language=self.language)
        # Check if the book and language are correctly linked
        self.assertEqual(book_language.book, self.book)
        self.assertEqual(book_language.language, self.language)
        
        
    def test_format_relation(self):
        # Create a Format instance linking the book and format
        format_instance = Format.objects.create(book=self.book, mime_type="text/plain", url="http://example.com/book.txt")
        
        # Check if the book and format are correctly linked
        self.assertEqual(format_instance.book, self.book)
        
        # Check if the format is included in the book's formats
        self.assertIn(format_instance, self.book.formats.all())

