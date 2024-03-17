from django.db import models


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    birth_year = models.SmallIntegerField(blank=True, null=True)
    death_year = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'books_author'


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    download_count = models.IntegerField(blank=True, null=True)
    gutenberg_id = models.IntegerField()
    media_type = models.CharField(max_length=16)
    title = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'books_book'


class BookAuthors(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='authors')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_authors'


class BookBookshelves(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookshelves')
    bookshelf = models.ForeignKey('Bookshelf', on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_bookshelves'


class BookLanguages(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='languages')
    language = models.ForeignKey('Language', on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_languages'


class BookSubjects(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_subjects'


class Bookshelf(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'books_bookshelf'


class Format(models.Model):
    id = models.AutoField(primary_key=True)
    mime_type = models.CharField(max_length=32)
    url = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='formats')

    class Meta:
        db_table = 'books_format'


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=4)

    class Meta:
        db_table = 'books_language'


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()

    class Meta:
        db_table = 'books_subject'
