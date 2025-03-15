from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Book
from api.serializers import BookSerializer

class BookAPITestCase(APITestCase):
    """
    Test cases for Book API endpoints
    """
    
    def setUp(self):
        """Set up test data and client"""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword',
            is_staff=True
        )
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Test Book 1',
            author='Test Author 1',
            isbn='1234567890123',
            price=19.99,
            publication_date='2023-01-01',
            genre='Fiction'
        )
        
        self.book2 = Book.objects.create(
            title='Test Book 2',
            author='Test Author 2',
            isbn='9876543210987',
            price=29.99,
            publication_date='2023-02-01',
            genre='Non-Fiction'
        )
        
        # URLs
        self.book_list_url = reverse('book-list')
        self.book_detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})
        
        # API client
        self.client = APIClient()
        
    def test_get_all_books_unauthenticated(self):
        """Test retrieving all books without authentication"""
        response = self.client.get(self.book_list_url)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_get_book_detail_unauthenticated(self):
        """Test retrieving a single book without authentication"""
        response = self.client.get(self.book_detail_url(self.book1.id))
        serializer = BookSerializer(self.book1)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication - should fail"""
        new_book_data = {
            'title': 'New Test Book',
            'author': 'New Test Author',
            'isbn': '5555555555555',
            'price': 15.99,
            'publication_date': '2023-03-01',
            'genre': 'Mystery'
        }
        
        response = self.client.post(self.book_list_url, new_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication"""
        self.client.force_authenticate(user=self.user)
        
        new_book_data = {
            'title': 'New Test Book',
            'author': 'New Test Author',
            'isbn': '5555555555555',
            'price': 15.99,
            'publication_date': '2023-03-01',
            'genre': 'Mystery'
        }
        
        response = self.client.post(self.book_list_url, new_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(isbn='5555555555555').title, 'New Test Book')
    
    def test_update_book_authenticated(self):
        """Test updating a book with authentication"""
        self.client.force_authenticate(user=self.user)
        
        updated_data = {
            'title': 'Updated Book Title',
            'price': 25.99
        }
        
        response = self.client.patch(self.book_detail_url(self.book1.id), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh from database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')
        self.assertEqual(self.book1.price, 25.99)
    
    def test_delete_book_authenticated(self):
        """Test deleting a book with authentication"""
        self.client.force_authenticate(user=self.user)
        
        initial_count = Book.objects.count()
        response = self.client.delete(self.book_detail_url(self.book1.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), initial_count - 1)
    
    def test_filtering_books(self):
        """Test filtering books by genre"""
        url = f"{self.book_list_url}?genre=Fiction"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 1')
    
    def test_searching_books(self):
        """Test searching books by title or author"""
        url = f"{self.book_list_url}?search=Author 2"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 2')
    
    def test_ordering_books(self):
        """Test ordering books by price descending"""
        url = f"{self.book_list_url}?ordering=-price"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 2')
        self.assertEqual(response.data['results'][1]['title'], 'Test Book 1')
    
    def test_admin_permissions(self):
        """Test that admin users have additional permissions"""
        # Regular user can't access admin-only endpoint (assuming you have one)
        self.client.force_authenticate(user=self.user)
        admin_url = reverse('admin-books')  # You would need to create this endpoint
        
        response = self.client.get(admin_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin user can access
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(admin_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)