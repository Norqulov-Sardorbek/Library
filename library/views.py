from datetime import timezone

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from library.models import Books
from library.permissions import IsAdmin, IsOperator, IsUser
from library.serializer import BookSerializer


# Create your views here.


class BookCreateAPIView(CreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdmin|IsOperator]

class BookReadAPIView(RetrieveAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
class BookUpdateAPIView(UpdateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdmin|IsOperator]
class BookDeleteAPIView(DestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdmin|IsOperator]

class OrderBookAPIView(APIView):
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        book_id = self.kwargs.get('book_id')
        book = Books.objects.get(id=book_id)
        if book and book.booked:
            return Response({'error': 'Kitob allaqachon band qilingan'}, status=status.HTTP_400_BAD_REQUEST)
        book.booked_date = timezone.now()
        book.booked_person = request.user
        book.save()
        return Response({'success': "Kitob siz uchun band qilindi"},status=status.HTTP_200_OK)
class TakeBookAPIView(APIView):
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Books, id=self.kwargs.get('book_id'))
        if not book.booked or book.booked_person != request.user:
            return Response({'error': 'Siz bu kitobni olish uchun band qilmagansiz'}, status=status.HTTP_400_BAD_REQUEST)
        book.taken = True
        book.booked_date = timezone.now()
        book.save()
        return Response({'message': 'Kitob muvaffaqiyatli olindi'}, status=status.HTTP_200_OK)

class ReturnBookAPIView(APIView):
    serializer_class = BookSerializer
    def post(self, request, *args, **kwargs):
        book_id = self.kwargs.get('book_id')
        book = Books.objects.get(id=book_id)
        if book and book.booked and book.booked_person != request.user:
            return Response({'error':"Kitob sizda emas"},status=status.HTTP_400_BAD_REQUEST)
        book.taken=False
        book.booked_date=None
        book.booked_person = None
        book.save()
        return Response({'message': f'Kitob muvaffaqiyatli topshirildi. Sizdan {book.total_payment} som boldi.'}, status=status.HTTP_200_OK)




