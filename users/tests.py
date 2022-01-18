import datetime

import pytz
from unittest.mock import MagicMock, patch
from django.test import TestCase, Client

from users.models import User
from orders.models import Order
from flights.models import Aircraft, Airline, Category, City, Seat, Flight, FlightSeat

class AuthorizationViewTest(TestCase):
    @patch('users.views.requests')
    def test_success_authorization_view_post_method(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                data = {
                    "id":123456789,
                    "properties": {
                        "nickname": "홍길동",
                    },
                    "kakao_account": {
                        "email":"sample@sample.com",
                    }
                }
                return data

            def raise_for_status(self):
                pass

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization": "access token"}
        response            = client.post("/users/authorize", **headers)

        self.assertEqual(response.status_code, 201)

    @patch("users.views.requests")
    def test_no_token_authorization_view_post_method(self, mocked_requests):
        client = Client()
        class MockedResponse:
            def json(self):
                data = {
                    "id":123456789,
                    "properties":{
                        "nickname":"홍길동"
                    },
                    "kakao_account":{
                        "email":"sample@sample.com",
                    },
                }
                return data
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_NoAuthorization":"access token"}
        response            = client.post("/users/authorize", **headers)

        self.assertEqual(response.status_code, 401)

    @patch("users.views.requests")
    def test_signin_kakao_view_post_invalid_token(self, mocked_requests):
        client = Client()
        class MockedResponse:
            def json(self):
                data = {
                    "error":12347,
                }
                return data
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization":"fake access token"}
        response            = client.post("/users/authorize", **headers)

        self.assertEqual(response.status_code, 403)


class UserOrderViewTest(TestCase):
    def setup(self):
        User.objects.create(
            id=1,
            kakao_id=122121,
            nickname="홍길동"
        )
        Order.objects.create(
            id=1,
            order_number=12345678,
            total_price=129000,
            created_at="",
            number_of_tickets=1,
            payments_method="카드",
            user_id = 1
        )
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
            price=129000,
            flight_id=1,
            seat_id=1
        )


    def test_success_mypage_get_method_test(self):
        client = Client()
        response = client.get('/users/mypage')

        data = {
            "id": 1,
            "reservation_number": 12345678,
            "flights": [
                {
                    "title": "[민석항공] 김포 - 제주", # [민석항공] 김포 - 제주
                    "travel_date": "2022-1-17",
                    "logo": "https://postfiles.pstatic.net/MjAyMjAxMTJfMjM5/MDAxNjQxOTg2NDgyNTY1.j1EtZziHhsuxfoRqmswcZFBZw4TQLdlPgD76IUviWU0g.Qf4_r2cIET-8Aox-iDTUpR9pSX2JcedcCrenLYMK-zIg.PNG.leecj0805/ms.png?type=w966"
                }
            ],
            "total_price": 129000,
            "number_of_tickets": 1,
            "payments_method": "카드",
        }


        result = {
            "type": "order_list",
            "data": data
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': result})
