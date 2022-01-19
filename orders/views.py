import json
import string
import random
import uuid

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction

from flights.models import FlightSeat
from orders.models  import Order, OrderItems
from users.models   import User

class OrderView(View):
    @login_required
    @transaction.atomic
    def post(self, request):
        try:
            data = json.loads(request.body)

            passengers        = data["passengerInfo"]
            email             = data["email"]
            phone_number      = data["phone_number"]
            name              = data["name"]
            total_price       = data["total_price"]
            number_of_tickets = data["number_of_tickets"]
            payments_method   = data["payments_method"]

            user = request.user

            #uuid로 주문번호


            # string_num = string.digits
            # random_length = 4
            # random_digits = ""

            # for i in range(random_length):
            #     random_digits += random.choice(string_num)

            # order_number = random_digits+"-"+phone_number[-4:]
            order_number = str(uuid.uuid4())

            order = Order.objects.create(
                order_number      = order_number,
                total_price       = total_price,
                number_of_tickets = number_of_tickets,
                payments_method   = payments_method,
                user              = user
            )

            
            for passenger in passengers:
                OrderItems.objects.create(
                    family_name    = passenger["family_name"],
                    given_name     = passenger["given_name"],
                    nationality    = passenger["nationality"],
                    sex            = passenger["sex"],
                    birthday       = passenger["birthday"],
                    order          = order,
                    flight_seat_id = passenger["flight_seat"]
                )
                
            return JsonResponse({"message" : "SUSSESS"}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)