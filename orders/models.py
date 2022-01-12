from users.models   import User
from flights.models import Flight_seat

from django.db                       import models
from django.db.models.fields         import DateTimeField, IntegerField
from django.db.models.fields.related import ForeignKey
from django.db.models.deletion       import CASCADE


class Order(models.Model):
    order_number      = models.CharField(max_length=100, unique=True)
    total_price       = models.DecimalField()
    number_of_tickets = models.IntegerField()
    payments_method   = models.CharField(max_length=50, default="카드")
    created_at        = models.DateTimeField(auto_now_add=True)
    user              = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

class OrderItems(models.Model):
    family_name = models.CharField(max_length=50)
    given_name  = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    sex         = models.CharField(max_length=20)
    birthday    = models.DateTimeField()
    order       = models.ForeignKey(Order, on_delete=models.CASCADE)
    flight_seat = models.ForeignKey(Flight_seat, on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_items'