# urls.py
from django.urls import path, include
from .views import BookQueryView

urlpatterns = [
    path('books/', BookQueryView.as_view(), name='book_query'),
    path("__debug__/", include("debug_toolbar.urls"))
]
