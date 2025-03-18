from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='posts'),
    path('register/', views.register, name='register'),  # URL for user registration
    path('login/', views.user_login, name='login'),  # URL for user login
    path('logout/', views.user_logout, name='logout'),  # URL for user logout
    path('profile/', views.profile, name='profile'),  # URL for user profile
  
]