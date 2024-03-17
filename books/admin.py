from django.contrib import admin
from .models import *
# Register your models here.
all_models = [Author, Book, BookAuthors, BookBookshelves, BookLanguages, BookSubjects , Format, Subject, Language, Bookshelf]
admin.site.register(all_models)
