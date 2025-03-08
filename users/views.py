from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from subscriptions.models import Subscription
from django.contrib import messages
from django.utils import timezone


def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Minimal validation, you can expand as needed
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, password=password)
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    return render(request, 'users/register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    sub = None
    try:
        sub = Subscription.objects.get(user=request.user)
    except Subscription.DoesNotExist:
        pass

    return render(request, 'users/profile.html', {'subscription': sub})
