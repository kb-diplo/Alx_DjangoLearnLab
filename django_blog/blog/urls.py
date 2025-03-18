from django.urls import path
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, post_detail, comment_edit, comment_delete
)

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),  # Create a new post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # View a single post
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),  # Update a post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # Delete a post
    path('', PostListView.as_view(), name='post-list'),  # List all posts (home page)
    path('register/', views.register, name='register'),  # URL for user registration
    path('login/', views.user_login, name='login'),  # URL for user login
    path('logout/', views.user_logout, name='logout'),  # URL for user logout
    path('profile/', views.profile, name='profile'),  # URL for user profile
    path('posts/', PostListView.as_view(), name='post-list'),  # List all posts
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # View a single post
    path('posts/new/', PostCreateView.as_view(), name='post-create'),  # Create a new post
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),  # Update a post
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # Delete a post
    path('post/<int:pk>/', post_detail, name='post-detail'),
    path('comment/<int:pk>/edit/', comment_edit, name='comment-edit'),
    path('comment/<int:pk>/delete/', comment_delete, name='comment-delete'),
]