from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Category
from .forms import BookForm
from django.utils import timezone
from subscriptions.models import Subscription
from django.contrib.auth.decorators import login_required
from .utils import get_subscribed_user_books  # Import your utils
from subscriptions.utils import has_active_subscription  # Import subscription utils

def home(request):
    categories = Category.objects.all()
    books = Book.objects.all()

    # Filter books based on subscription status
    visible_books = get_subscribed_user_books(request.user, books)

    # Check if user has an active subscription for template
    has_subscription = has_active_subscription(request.user)

    context = {
        'categories': categories,
        'books': visible_books,
        'has_subscription': has_subscription
    }
    return render(request, 'books/home.html', context)

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    books_in_category = Book.objects.filter(category=category)

    return render(request, 'books/category_detail.html', {
        'category': category,
        'books_in_category': books_in_category
    })

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book': book
    }
    return render(request, 'books/book_detail.html', context)

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

@login_required
def read_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    # Check if the book is premium and the user has an active subscription
    if book.is_premium:
        try:
            sub = Subscription.objects.get(user=request.user)
            if not sub.is_active():
                # User is not subscribed; redirect to subscribe page with a message.
                return redirect('subscribe')
        except Subscription.DoesNotExist:
            return redirect('subscribe')

    return render(request, 'books/book_read.html', {'book': book})