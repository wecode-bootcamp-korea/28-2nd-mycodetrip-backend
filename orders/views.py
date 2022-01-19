import json
import string
import random

from django.http.response import JsonResponse

from django.views import View
from flights.models import FlightSeat

from orders.models import Order, OrderItems
from users.models import User

class OrderView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            passengerInfo     = data["passengerInfo"]
            email             = data["email"]
            phone_number      = data["phone_number"]
            name              = data["name"]
            total_price       = data["total_price"]
            number_of_tickets = data["number_of_tickets"]
            payments_method   = data["payments_method"]
            # family_name       = data["family_name"]
            # given_name        = data["given_name"]
            # nationality       = data["nationality"]
            # sex               = data["sex"]
            # birthday          = data["birthday"]
            # flight_seat       = data["flight_seat"]
            nickname          = data["nickname"]
            kakao_id          = data["kakao_id"]
            

            user, is_created = User.objects.get_or_create(
                email = email,
                phone_number = phone_number,
                name = name,
                nickname = nickname,
                kakao_id = kakao_id
            )

            string_num = string.digits
            random_length = 4
            random_digits = ""

            for i in range(random_length):
                random_digits += random.choice(string_num)

            order_number = random_digits+"-"+phone_number[-4:]

            order = Order.objects.create(
                order_number = order_number,
                total_price = total_price,
                number_of_tickets = number_of_tickets,
                payments_method = payments_method,
                user = user
            )

            
            for passenger in passengerInfo:
                OrderItems.objects.create(
                    family_name = passenger["family_name"],
                    given_name = passenger["given_name"],
                    nationality = passenger["nationality"],
                    sex = passenger["sex"],
                    birthday = passenger["birthday"],
                    order = order,
                    flight_seat = FlightSeat.objects.get(id=1)
                )
                
            return JsonResponse({"message" : "SUSSESS"}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR!!!!!!"}, status=400)