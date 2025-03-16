from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Book


class BookAPITestCase(APITestCase):
    """Test suite for Book API endpoints"""

    def setUp(self):
        """
        Set up test data and authentication
        """
        # Create test users
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='user123'
        )
        
        # Create initial books
        self.book1 = Book.objects.create(
            title='Test Book 1',
            author='Author 1',
            publication_date='2023-01-01',
            isbn='1234567890123',
            price=19.99
        )
        self.book2 = Book.objects.create(
            title='Test Book 2',
            author='Author 2',
            publication_date='2023-02-01',
            isbn='1234567890124',
            price=29.99
        )
        
        # Set up API client
        self.client = APIClient()
        
        # API endpoints
        self.book_list_url = reverse('book-list')
        self.book_detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})
    
    def test_get_book_list(self):
        """Test retrieving a list of books"""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_book_detail(self):
        """Test retrieving a specific book"""
        response = self.client.get(self.book_detail_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book 1')
        self.assertEqual(response.data['author'], 'Author 1')
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication"""
        self.client.force_authenticate(user=self.admin_user)
        new_book_data = {
            'title': 'New Test Book',
            'author': 'New Author',
            'publication_date': '2023-03-01',
            'isbn': '1234567890125',
            'price': 39.99
        }
        response = self.client.post(self.book_list_url, new_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Test Book')
        self.assertEqual(Book.objects.count(), 3)
    
    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication"""
        new_book_data = {
            'title': 'Unauthorized Book',
            'author': 'Unauthorized Author',
            'publication_date': '2023-03-01',
            'isbn': '1234567890126',
            'price': 39.99
        }
        response = self.client.post(self.book_list_url, new_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 2)  # No new book added
    
    def test_update_book(self):
        """Test updating a book"""
        self.client.force_authenticate(user=self.admin_user)
        updated_data = {
            'title': 'Updated Book Title',
            'price': 24.99
        }
        response = self.client.patch(self.book_detail_url(self.book1.pk), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book Title')
        self.assertEqual(response.data['price'], '24.99')
        
        # Verify in database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')
    
    def test_delete_book(self):
        """Test deleting a book"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.book_detail_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
    
    def test_filter_books(self):
        """Test filtering books by various parameters"""
        # Create additional books for filtering
        Book.objects.create(
            title='Python Book',
            author='Python Author',
            publication_date='2023-04-01',
            isbn='1234567890127',
            price=49.99
        )
        
        # Test filtering by title
        response = self.client.get(f"{self.book_list_url}?title__icontains=python")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Python Book')
        
        # Test filtering by price range
        response = self.client.get(f"{self.book_list_url}?price__gte=25")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Test multiple filters
        response = self.client.get(f"{self.book_list_url}?author__icontains=author&price__lt=30")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_ordering_books(self):
        """Test ordering books by various fields"""
        # Test ordering by price ascending
        response = self.client.get(f"{self.book_list_url}?ordering=price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [float(book['price']) for book in response.data]
        self.assertEqual(prices, sorted(prices))
        
        # Test ordering by price descending
        response = self.client.get(f"{self.book_list_url}?ordering=-price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [float(book['price']) for book in response.data]
        self.assertEqual(prices, sorted(prices, reverse=True))
        
        # Test ordering by title
        response = self.client.get(f"{self.book_list_url}?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_search_books(self):
        """Test searching books"""
        # Assuming you have a search filter set up in your viewset
        Book.objects.create(
            title='Django for Beginners',
            author='Author 3',
            publication_date='2023-05-01',
            isbn='1234567890128',
            price=34.99
        )
        
        # Test search by title
        response = self.client.get(f"{self.book_list_url}?search=django")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django for Beginners')
        
        # Test search by author
        response = self.client.get(f"{self.book_list_url}?search=author")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 3)
    
    def test_permissions(self):
        """Test permission controls"""
        # Unauthenticated user should be able to list books
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Unauthenticated user should not be able to create a book
        new_book_data = {
            'title': 'Permission Test Book',
            'author': 'Permission Test Author',
            'publication_date': '2023-06-01',
            'isbn': '1234567890129',
            'price': 19.99
        }
        response = self.client.post(self.book_list_url, new_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Regular user may or may not have permission to create a book (depends on your permission setup)
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(self.book_list_url, new_book_data, format='json')
        # This assumes regular users can't create books - adjust based on your permissions
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_201_CREATED])
