from django.urls import path, include
from .views import activation, BooksList, BooksDetail, BookCreate, BookUpdate, BookDelete, CommentCreate, CommentsList, CommentAccept, CommentDelete


urlpatterns = [
   path('activation/', activation, name='activation'),
   path('books/', BooksList.as_view(), name= 'books_list'),
   path('books/<int:pk>/', BooksDetail.as_view(), name= 'books_detail'),
   path('books/create/', BookCreate.as_view(), name='book_create'),
   path('books/<int:pk>/edit/', BookUpdate.as_view(), name='book_update'),
   path('books/<int:pk>/delete/', BookDelete.as_view(), name='book_delete'),
   path('comments/', CommentsList.as_view(), name= 'comments_list'),
   path('comments/create/', CommentCreate.as_view(), name='book_create'),
   path('comments/update/<int:pk>/', CommentAccept.as_view(), name='comment_accept'),
   path('comments/delete/<int:pk>/', CommentDelete.as_view(), name='comment_delete'),

]