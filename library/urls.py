from django.urls import path

from library.views import BookCreateAPIView, BookReadAPIView, BookUpdateAPIView, BookDeleteAPIView, OrderBookAPIView, \
    TakeBookAPIView,ReturnBookAPIView

urlpatterns = [
    path('book-create/', BookCreateAPIView.as_view(), name='book-create'),
    path('book-read/', BookReadAPIView.as_view(), name='book-read'),
    path('book-update/<int:pk>/', BookUpdateAPIView.as_view(), name='book-update'),
    path('book-delete/<int:pk>/', BookDeleteAPIView.as_view(), name='book-delete'),
    path('book-reserve/<int:book_id>/',OrderBookAPIView.as_view(),name='book-reserve'),
    path('book-take/<int:book_id>/', TakeBookAPIView.as_view(), name='book-take'),
    path('book-return/<int:book_id>/', ReturnBookAPIView.as_view(), name='book-return'),
]
