from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated ,AllowAny
from rest_framework.filters import OrderingFilter ,SearchFilter
from django_filters.rest_framework import DjangoFilterBackend 

# BookListView: Retrieve all books (public access)
class BookListView(generics.ListAPIView):
    """
    Retrieve a list of books with filtering, searching, and ordering capabilities.
    - Filter by: title, author name, publication year.
    - Search by: title, author name.
    - Order by: title, publication year.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] 
    filterset_fields = ['title', 'author__name', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year'] 

# BookDetailView: Retrieve a single book by ID (public access)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

# BookCreateView: Add a new book (authenticated users only)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Custom logic before saving the book
        serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Customize the response
        return Response({"message": "Book created successfully!", "data": response.data}, status=status.HTTP_201_CREATED)

# BookUpdateView: Modify an existing book (authenticated users only)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Custom logic before updating the book
        serializer.save()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        # Customize the response
        return Response({"message": "Book updated successfully!", "data": response.data}, status=status.HTTP_200_OK)

# BookDeleteView: Remove a book (authenticated users only)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]