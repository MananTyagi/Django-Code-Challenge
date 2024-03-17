from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Book

class BookListAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book1 = Book.objects.create(title='Test Book 1')
        self.book2 = Book.objects.create(title='Test Book 2')

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    # Add more test cases as needed...
