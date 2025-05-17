
from rest_framework import serializers
from .models import Books, Rating

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'books', 'rating']

class BookSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(read_only=True)
    total_payment = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Books
        fields = ['id', 'title', 'book_file', 'taken', 'borrowing_price', 'booked_date', 'booked_person', 'rating', 'total_payment']



