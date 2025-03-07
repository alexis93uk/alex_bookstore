from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Category
from .forms import BookForm

def home(request):
    categories = Category.objects.all()
    books = Book.objects.all()
    context = {
        'categories': categories,
        'books': books,
    }
    return render(request, 'books/home.html', context)

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    books = Book.objects.filter(category=category)
    context = {
        'category': category,
        'books': books,
    }
    return render(request, 'books/category_detail.html', context)

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