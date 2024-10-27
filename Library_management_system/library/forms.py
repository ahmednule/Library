from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Book, BorrowedBook

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_date', 'available_copies']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'})
        }

class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = ['return_date']
        widgets = {
            'return_date': forms.DateInput(attrs={'type': 'date'})
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)
