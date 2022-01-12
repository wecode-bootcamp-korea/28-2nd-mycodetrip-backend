from django.db  import models

class Flight(models.Model):
    departure_time = models.DateTimeField()
    arrival_time   = models.DateTimeField()
    flight_time    = models.CharField(max_length=50)
    seats          = models.ManyToManyField("Seat", through="FlightSeat")
    departure_city = models.ForeignKey("City", on_delete=models.CASCADE, related_name="departure_flight")
    arrival_city   = models.ForeignKey("City", on_delete=models.CASCADE, related_name="arrival_flight")
    aircraft       = models.ForeignKey("Aircraft", on_delete=models.CASCADE)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'flights'

class FlightSeat(models.Model):
    stock  = models.IntegerField()
    price  = models.DecimalField(max_digits=10, decimal_places=2)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat   = models.ForeignKey("Seat", on_delete=models.CASCADE)

    class Meta:
        db_table = 'flights_seats'

class Seat(models.Model):
    type = models.CharField(max_length=20)

    class Meta:
        db_table = 'seats'

class City(models.Model):
    name     = models.CharField(max_length=50)
    code     = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    class Meta:
        db_table = 'cities'

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'categories'

class Aircraft(models.Model):
    code    = models.CharField(max_length=20, unique=True)
    airline = models.ForeignKey("Airline", on_delete=models.CASCADE)

    class Meta:
        db_table = 'aircrafts'

class Airline(models.Model):
    name = models.CharField(max_length=40, unique=True)
    logo = models.CharField(max_length=1000)

    class Meta:
        db_table = 'airlines'

class Thumbnail(models.Model):
    image = models.CharField(max_length=1000)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        db_table = 'thumbnails'