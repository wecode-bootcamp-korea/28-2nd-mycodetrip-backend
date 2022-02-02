import jwt
import datetime
import pytz

import requests
from django.http import JsonResponse
from django.views import View

from users.models import User
from orders.models import Order
from mycodetrip.config import SECRET_KEY
from users.decorator import login_required


class AuthorizationView(View):
    def post(self, request):
        try:
            # 1. frontend로부터 access token을 받음
            access_token = request.headers.get("Authorization", None)
            if not access_token:
                return JsonResponse({"message":"NO_TOKEN"}, status=401)

            # 2. access token 이용해 카카오로부터 유저 정보 받아옴
            headers = {
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                "Authorization": f'Bearer {access_token}'
            }
            response = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)
            response = response.json()
            kakao_id = response.get("id", None)

            if not kakao_id:
                return JsonResponse({"message":"INVALID_TOKEN"}, status=403)

            nickname = response["properties"]["nickname"]
            email    = response["kakao_account"].get("email")

            # 3. 회원가입 or 로그인
            user, is_created = User.objects.get_or_create(
                kakao_id=kakao_id, # unique한 값만 넣어야한다.
                defaults={
                    "nickname": nickname,
                    "email": email
                }
            )

            now = datetime.datetime.now(pytz.utc)

            payload = {
                "id" : user.id,
                "exp": now + datetime.timedelta(days=7),
                "iat": now,
            }
            access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            if is_created:
                status = 201
            else:
                status = 200

            return JsonResponse({"jwt_token": access_token}, status=status)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

class UserOrderView(View):
    @login_required
    def get(self, request):
        orders = Order.objects.filter(user_id=request.user.id).order_by("-created_at", "id")

        result = {
            "type": "order_list",
            "data": [{
                "id"                 : order.id,
                "reservation_number" : order.order_number,
                "total_price"        : int(order.total_price),
                "number_of_tickets"  :order.number_of_tickets,
                "flights" : [{
                    "id"         : order_item.flight_seat.id,
                    "airline"    : order_item.flight_seat.flight.aircraft.airline.name,
                    "departure"  : order_item.flight_seat.flight.departure_city.name,
                    "arrival"    : order_item.flight_seat.flight.arrival_city.name,
                    "travel_date": (order_item.flight_seat.flight.departure_time).date(),
                    "logo"       : order_item.flight_seat.flight.aircraft.airline.logo
                } for order_item in order.orderitems_set.order_by("flight_seat__flight__departure_time")]
            } for order in orders]
        }

        return JsonResponse({"result": result}, status=200)
