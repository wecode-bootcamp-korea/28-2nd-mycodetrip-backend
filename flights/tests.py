import datetime
import pytz

from django.test import TestCase, Client

from flights.models import Category, Flight, FlightSeat, Seat, Aircraft, Airline, City, Thumbnail

NOW = datetime.datetime.now(pytz.utc)
class FlightListTest(TestCase):
    def setUp(self):
        Airline.objects.create(
            id=1,
            name="민석항공",
            logo="https://postfiles.pstatic.net/MjAyMjAxMTJfMjM5/MDAxNjQxOTg2NDgyNTY1.j1EtZziHhsuxfoRqmswcZFBZw4TQLdlPgD76IUviWU0g.Qf4_r2cIET-8Aox-iDTUpR9pSX2JcedcCrenLYMK-zIg.PNG.leecj0805/ms.png?type=w966"
        )
        Aircraft.objects.create(id=1, code="MS999", airline_id=1)
        Category.objects.create(id=1, name="아시아")
        City.objects.create(id=1, name="김포", code="GMP", category_id=1)
        City.objects.create(id=2, name="제주", code="CJU", category_id=1)
        Seat.objects.create(id=1, type="비즈니스")

        Flight.objects.create(
            id=1,
            departure_time=datetime.datetime(2022, 1, 17, 6, 24, 35, tzinfo=pytz.utc),
            arrival_time=datetime.datetime(2022, 1, 17, 6, 24, 35, tzinfo=pytz.utc)+ datetime.timedelta(hours=3),
            flight_time=3,
            departure_city_id=1,
            arrival_city_id=2,
            aircraft_id=1
        )
        FlightSeat.objects.create(
            id=1,
            stock=3,
            price=139000,
            flight_id=1,
            seat_id=1
        )

    def test_success_flight_list_view_get_method(self):
        client = Client()
        response = client.get('/flights',
            {
                "departure_date": "2022-01-17",
                "arrival_date"  : "2022-01-17",
                "departure_city": "김포",
                "arrival_city"  : "제주"
            }
        )

        result = {
            "total": 1,
            "departure_date": "2022-01-17",
            "arrival_date": "2022-01-17",
            "type": "flight_list",
            "data": [{
                "id": 1,
                "flight_time": 3,
                "airline"    : "민석항공",
                "aircraft"   : "MS999",
                "logo"       : "https://postfiles.pstatic.net/MjAyMjAxMTJfMjM5/MDAxNjQxOTg2NDgyNTY1.j1EtZziHhsuxfoRqmswcZFBZw4TQLdlPgD76IUviWU0g.Qf4_r2cIET-8Aox-iDTUpR9pSX2JcedcCrenLYMK-zIg.PNG.leecj0805/ms.png?type=w966",
                "price"      : 139000,
                "tickets"    : 3,
                "seat_type"  : 1,
                "departure": {
                    "time": '2022-01-17T06:24:35Z',
                    "city": "김포",
                    "code": "GMP",
                },
                "arrival": {
                    "time": '2022-01-17T09:24:35Z',
                    "city": "제주",
                    "code": "CJU",
                }
            }],
        }


        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': result})


    def tearDown(self):
        Airline.objects.all().delete()
        Aircraft.objects.all().delete()
        Category.objects.all().delete()
        City.objects.all().delete()
        Seat.objects.all().delete()
        Flight.objects.all().delete()
        FlightSeat.objects.all().delete()

class CityListViewTest(TestCase):
    def setUp(self):
        Category.objects.create(id=1, name="아시아")
        City.objects.create(id=1, name="제주", code="CJU", category_id=1)
        City.objects.create(id=2, name="김포", code="GMP", category_id=1)


    def test_success_city_list_view_get_method(self):
        client = Client()
        response = client.get('/flights/cities')

        result = {
            "type": "city_list",
            "data":[
                {
                    "id": 1,
                    "category": "아시아",
                    "city": [
                        {"id":1, "name":"제주", "code":"CJU", "category_id":1},
                        {"id":2, "name":"김포", "code":"GMP", "category_id":1}
                    ]
                }
            ]
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': result})

    def tearDown(self):
        Category.objects.all().delete()
        City.objects.all().delete()

class AirlineListViewTest(TestCase):
    def setUp(self):
        Airline.objects.create(
            id=1,
            name="찬주프로",
            logo="https://postfiles.pstatic.net/MjAyMjAxMTJfMjM5/MDAxNjQxOTg2NDgyNTY1.j1EtZziHhsuxfoRqmswcZFBZw4TQLdlPgD76IUviWU0g.Qf4_r2cIET-8Aox-iDTUpR9pSX2JcedcCrenLYMK-zIg.PNG.leecj0805/ms.png?type=w966"
        )
        Airline.objects.create(
            id=2,
            name="민석항공",
            logo="https://postfiles.pstatic.net/MjAyMjAxMTJfMjM5/MDAxNjQxOTg2NDgyNTY1.j1EtZziHhsuxfoRqmswcZFBZw4TQLdlPgD76IUviWU0g.Qf4_r2cIET-8Aox-iDTUpR9pSX2JcedcCrenLYMK-zIg.PNG.leecj0805/ms.png?type=w966"
        )
        Airline.objects.create(
            id=3,
            name="준영항공",
            logo="https://postfiles.pstatic.net/MjAyMjAxMTJfMjM5/MDAxNjQxOTg2NDgyNTY1.j1EtZziHhsuxfoRqmswcZFBZw4TQLdlPgD76IUviWU0g.Qf4_r2cIET-8Aox-iDTUpR9pSX2JcedcCrenLYMK-zIg.PNG.leecj0805/ms.png?type=w966"
        )

    def test_success_airline_list_view_get_method(self):
        client = Client()
        response = client.get('/flights/airlines')

        result = {
            "type": "airline_list",
            "data": [
                {
                "id": 1,
                "name": "찬주프로",
                "logo": "https://postfiles.pstatic.net/MjAyMjAxMTJfMjM5/MDAxNjQxOTg2NDgyNTY1.j1EtZziHhsuxfoRqmswcZFBZw4TQLdlPgD76IUviWU0g.Qf4_r2cIET-8Aox-iDTUpR9pSX2JcedcCrenLYMK-zIg.PNG.leecj0805/ms.png?type=w966",
                },
                {
                "id": 2,
                "name": "민석항공",
                "logo": "https://postfiles.pstatic.net/MjAyMjAxMTJfMjM5/MDAxNjQxOTg2NDgyNTY1.j1EtZziHhsuxfoRqmswcZFBZw4TQLdlPgD76IUviWU0g.Qf4_r2cIET-8Aox-iDTUpR9pSX2JcedcCrenLYMK-zIg.PNG.leecj0805/ms.png?type=w966",
                },
                {
                "id": 3,
                "name": "준영항공",
                "logo": "https://postfiles.pstatic.net/MjAyMjAxMTJfMjM5/MDAxNjQxOTg2NDgyNTY1.j1EtZziHhsuxfoRqmswcZFBZw4TQLdlPgD76IUviWU0g.Qf4_r2cIET-8Aox-iDTUpR9pSX2JcedcCrenLYMK-zIg.PNG.leecj0805/ms.png?type=w966",
                }
            ]
        }

    def tearDown(self):
        Airline.objects.all().delete()


class SeatTypeViewTest(TestCase):
    def setUp(self):
        Seat.objects.create(id=1, type="이코노미")
        Seat.objects.create(id=2, type="비즈니스")
        Seat.objects.create(id=3, type="퍼스트")

    def test_success_seat_type_view_get_method(self):
        client = Client()
        response = client.get('/flights/seats')

        result = {
            "type": "seat_type",
            "data": [
                {
                "id"  : 1,
                "name": "이코노미",
                },
                {
                "id"  : 2,
                "name": "비즈니스",
                },
                {
                "id"  : 2,
                "name": "퍼스트",
                }
            ]
        }

    def tearDown(self):
        Seat.objects.all().delete()

class MainViewTest(TestCase):
    def setUp(self):
        Flight.objects.create(
            id=1,
            departure_time=datetime.datetime(2022, 1, 19, 6, 24, 35, tzinfo=pytz.utc),
            arrival_time=datetime.datetime(2022, 1, 19, 6, 24, 35, tzinfo=pytz.utc)+ datetime.timedelta(hours=3),
            flight_time=3,
            departure_city_id=1,
            arrival_city_id=2,
            aircraft_id=1
            )

        Thumbnail.objects.create(
            id=1,
            image="https://postfiles.pstatic.net/MjAyMjAxMTJfMjM5/MDAxNjQxOTg2NDgyNTY1.j1EtZziHhsuxfoRqmswcZFBZw4TQLdlPgD76IUviWU0g.Qf4_r2cIET-8Aox-iDTUpR9pSX2JcedcCrenLYMK-zIg.PNG.leecj0805/ms.png?type=w966",
            city_id=1
            )
        Aircraft.objects.create(id=1, code="MS999", airline_id=1)
        Category.objects.create(id=1, name="아시아")
        City.objects.create(id=1, name="김포", code="GMP", category_id=1)
        City.objects.create(id=2, name="제주", code="CJU", category_id=1)
        Seat.objects.create(id=1, type="비즈니스")
        FlightSeat.objects.create(
            id=1,
            stock=3,
            price=139000,
            flight_id=1,
            seat_id=1
        )
        Airline.objects.create(
            id=1,
            name="찬주프로",
            logo="https://postfiles.pstatic.net/MjAyMjAxMTJfMjM5/MDAxNjQxOTg2NDgyNTY1.j1EtZziHhsuxfoRqmswcZFBZw4TQLdlPgD76IUviWU0g.Qf4_r2cIET-8Aox-iDTUpR9pSX2JcedcCrenLYMK-zIg.PNG.leecj0805/ms.png?type=w966"
        )
        
    def test_sussess_main_view_get_method(self):
        client = Client()
        response = client.get('/flights/main')

        result = {
            "city" : "제주",
            "data" : [
                {
                "id"             : 1,
                "image"          : "https://postfiles.pstatic.net/MjAyMjAxMTJfMjM5/MDAxNjQxOTg2NDgyNTY1.j1EtZziHhsuxfoRqmswcZFBZw4TQLdlPgD76IUviWU0g.Qf4_r2cIET-8Aox-iDTUpR9pSX2JcedcCrenLYMK-zIg.PNG.leecj0805/ms.png?type=w966",
                "departure_city" : "김포",
                "arrival_city"   : "제주", 
                "departure_time" : "2022-01-19T06:24:35Z",
                "arrival_time"   : "2022-01-19T06:24:35Z",
                "price"          : 139000
                }
            ]}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': result})

    def tearDown(self):
        Flight.objects.all().delete()
        Thumbnail.objects.all().delete()
        Airline.objects.all().delete()
        Aircraft.objects.all().delete()
        Category.objects.all().delete()
        City.objects.all().delete()
        Seat.objects.all().delete()
        FlightSeat.objects.all().delete()