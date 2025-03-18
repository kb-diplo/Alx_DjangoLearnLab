from django.shortcuts import render

def home(request):
    return render(request, 'blog/home.html')

def post_list(request):
    return render(request, 'blog/post_list.html')

def user_login(request):
    return render(request, 'blog/login.html')

def register(request):
    return render(request, 'blog/register.html')