# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q  # Import Q for complex queries
from .models import Book
from .serializers import BookSerializer

class BookQueryView(APIView):
    def get(self, request):
        # Get queryset based on filters
        # books = Book.objects.all()
        books = Book.objects.prefetch_related('bookshelves', 'languages', 'subjects', 'formats', 'authors')
        
        # Apply filters based on query parameters
        for param, values in request.query_params.lists():
            if param == 'book_id':
                books = books.filter(gutenberg_id__in=values)
            elif param == 'language':
                books = books.filter(languages__language__code__in=values)
            elif param == 'mime_type':
                books = books.filter(formats__mime_type__in=values)
            elif param == 'topic':
                # Combine Q objects for subject and bookshelf filtering
                query = Q(subjects__subject__name__icontains=values[0]) | Q(bookshelves__bookshelf__name__icontains=values[0])
                for value in values[1:]:
                    query |= Q(subjects__subject__name__icontains=value) | Q(bookshelves__bookshelf__name__icontains=value)
                books = books.filter(query)
            elif param == 'author':
                books = books.filter(authors__author__name__icontains=values[0])
                for value in values[1:]:
                    books |= books.filter(authors__author__name__icontains=value)
            elif param == 'title':
                books = books.filter(title__icontains=values[0])
                for value in values[1:]:
                    books |= books.filter(title__icontains=value)

        # Order queryset by download count in descending order
        books = books.order_by('-download_count')

        # Initialize pagination
        paginator = PageNumberPagination()
        paginator.page_size = 20  # Number of books per page
        result_page = paginator.paginate_queryset(books, request)

        # Serialize paginated queryset
        serializer = BookSerializer(result_page, many=True)
        # print(books.count())
        # Return paginated response
        return paginator.get_paginated_response({
            'count': books.count(),  # Total number of books meeting the criteria
            'books': serializer.data
        })
