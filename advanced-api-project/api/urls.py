from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    # ListView: Retrieve all books
    path('books/', BookListView.as_view(), name='book-list'),

    # DetailView: Retrieve a single book by ID
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    # CreateView: Add a new book
    path('books/create/', BookCreateView.as_view(), name='book-create'),

    # UpdateView: Modify an existing book
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),

    # DeleteView: Remove a book
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]