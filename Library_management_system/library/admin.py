from django.contrib import admin
from .models import Book, BorrowedBook,Profile

admin.site.register(Book)
admin.site.register(BorrowedBook)
admin.site.register(Profile)