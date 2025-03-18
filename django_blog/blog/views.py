from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post


def home(request):
    return render(request, 'blog/home.html')

def post_list(request):
    return render(request, 'blog/post_list.html')

def register(request):
    # Handle user registration
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to the home page
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def user_login(request):
    # Handle user login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)  # Authenticate the user
        if user is not None:
            login(request, user)  
            return redirect('home')  
    return render(request, 'blog/login.html')

@login_required
def user_logout(request):
    # Handle user logout
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    # Handle profile updates
    if request.method == 'POST':
        user = request.user
        user.email = request.POST['email']  # Update the user's email
        user.save()
        return redirect('profile')  # Redirect back to the profile page
    return render(request, 'blog/profile.html')

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  
    context_object_name = 'posts'  
    ordering = ['-published_date']  # Order posts by published date (newest first)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']  
    template_name = 'blog/post_form.html' 

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author to the current user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content'] 
    template_name = 'blog/post_form.html'  

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Only the author can update the post

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'  
    success_url = reverse_lazy('post-list')  # Redirect to the post list after deletion

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Only the author can delete the post