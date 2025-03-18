from rest_framework import generics, filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author
from .serializers import BookSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny

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

    def put(self, request, *args, **kwargs):
        book_id = request.data.get('id')  # Get the book ID from the request data
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(book, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Book updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)

# BookDeleteView: Remove a book (authenticated users only)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        book_id = request.data.get('id')  # Get the book ID from the request data
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        book.delete()
        return Response({"message": "Book deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
