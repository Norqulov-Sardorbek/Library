from django.db import models
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from decimal import Decimal, ROUND_HALF_UP
# Create your models here.

User = get_user_model()

class Books(models.Model):
    title = models.CharField(max_length=100)
    book_file = models.FileField(upload_to='books/')
    taken=models.BooleanField(default=False)
    borrowing_price=models.DecimalField(decimal_places=2, max_digits=10)
    booked_date = models.DateTimeField(default=timezone.now,null=True,blank=True)
    booked_person = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.title

    @property
    def booked(self):
        if self.booked_date:
            return timezone.now() < self.booked_date + timedelta(days=1)
        return False

    @property
    def rating(self):
        return self.rating.aggregate(Avg('rating'))['rating__avg'] or None

    @property
    def total_payment(self):
        if not self.booked_date:
            return Decimal('0.00')
        now = timezone.now()
        delta = now - self.booked_date
        days_used = delta.days + 1
        price = self.borrowing_price * days_used
        overdue_days = max(0, days_used - 1)
        penalty = self.borrowing_price * Decimal('0.01') * overdue_days
        total = price + penalty
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class Rating(models.Model):
    books = models.ForeignKey(Books,related_name='rating', on_delete=models.CASCADE)
    rating = models.IntegerField()
