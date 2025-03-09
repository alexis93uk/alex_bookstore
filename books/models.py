from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=True)
    image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    full_text = models.TextField(blank=True, null=True, help_text="Full text of the book")

    def __str__(self):
        return self.title
