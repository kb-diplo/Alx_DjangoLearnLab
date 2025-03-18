from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


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
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to the home page
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