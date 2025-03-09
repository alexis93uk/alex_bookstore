from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),          
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('add-book/', views.add_book, name='add_book'),
    path('book/<int:pk>/read/', views.read_book, name='read_book'),
]
