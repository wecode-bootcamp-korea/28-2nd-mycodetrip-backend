import json
import uuid

from django.http.response import JsonResponse

from django.views import View
from flights.models import FlightSeat

from orders.models import Order, OrderItems
from users.decorator import login_required

class OrderView(View):
    @login_required
    def post(self, request):
        try:
            data = json.loads(request.body)

            passengers        = data["passengerInfo"]
            customer          = data["customer"]
            total_price       = data["total_price"]
            number_of_tickets = data["number_of_tickets"]
            payments_method   = data["payments_method"]
            flight_seats_id   = data["flight_seats_id"]

            user = request.user

            user.name         = customer["name"]
            user.email        = customer["email"]
            user.phone_number = customer["phonenumber"]
            user.save()            

            order_number = str(uuid.uuid4())

            order = Order.objects.create(
                order_number      = order_number,
                total_price       = total_price,
                number_of_tickets = number_of_tickets,
                payments_method   = payments_method,
                user              = user
            )
            
            for passenger in passengers:
                for id in flight_seats_id:
                    OrderItems.objects.create(
                        family_name = passenger["family_name"],
                        given_name  = passenger["given_name"],
                        nationality = passenger["nationality"],
                        sex         = passenger["sex"],
                        birthday    = passenger["birthday"],
                        order       = order,
                        flight_seat = FlightSeat.objects.get(id=id)
                    )
                
            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)