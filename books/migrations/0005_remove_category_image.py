# Generated by Django 5.1.7 on 2025-03-09 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_book_full_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='image',
        ),
    ]
