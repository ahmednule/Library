from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import Book, BorrowedBook
from .forms import BookForm, BorrowBookForm, CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('book_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    borrowed = BorrowedBook.objects.filter(book=book, user=request.user, returned=False).exists()
    
    if request.method == 'POST':
        form = BorrowBookForm(request.POST)
        if form.is_valid() and book.available_copies > 0:
            borrow = form.save(commit=False)
            borrow.user = request.user
            borrow.book = book
            borrow.save()
            
            book.available_copies -= 1
            book.save()
            
            messages.success(request, 'Book borrowed successfully!')
            return redirect('book_list')
    else:
        form = BorrowBookForm()
        
    return render(request, 'library/book_detail.html', {
        'book': book,
        'form': form,
        'borrowed': borrowed
    })

@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library/book_form.html', {'form': form})

@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form})

@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    return render(request, 'library/book_confirm_delete.html', {'book': book})

@login_required
def borrowed_books(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user, returned=False)
    return render(request, 'library/borrowed_books.html', {'borrowed_books': borrowed_books})

@login_required
def return_book(request, pk):
    borrowed_book = get_object_or_404(BorrowedBook, pk=pk, user=request.user)
    if request.method == 'POST':
        borrowed_book.returned = True
        borrowed_book.save()
        
        book = borrowed_book.book
        book.available_copies += 1
        book.save()
        
        messages.success(request, 'Book returned successfully!')
        return redirect('borrowed_books')
    return render(request, 'library/return_book_confirm.html', {'borrowed_book': borrowed_book})
