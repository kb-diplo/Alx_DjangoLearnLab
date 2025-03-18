from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='posts'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
]