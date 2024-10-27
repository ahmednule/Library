from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('signup/', views.signup, name='signup'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/new/', views.book_create, name='book_create'),
    path('book/<int:pk>/edit/', views.book_update, name='book_update'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('borrowed/', views.borrowed_books, name='borrowed_books'),
    path('borrowed/<int:pk>/return/', views.return_book, name='return_book'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
]