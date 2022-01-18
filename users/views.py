import datetime

from django.http import JsonResponse
from django.views import View

from orders.models import Order, OrderItems

class MyPageView(View):
    def get(self, request):
        orders = Order.objects.filter(user_id=request.user.id).order_by("-created_at", "id")

        data = []

        for order in orders:
            order_items = OrderItems.objects.filter(order_id=order.id).select_related("orders", "flights_seats")
            flight_seats = {item.flight_seat for item in order_items}
            flights = {s.flight for s in flight_seats}  # set comprehension
            flights = list(flights).sort(key=lambda x: x.departure_time)

            data.append(
                {
                    "id": order.id,
                    "reservation_number": order.order_number,
                    "flights": [
                        {
                            "title": f"[{flight.aircraft.airline.name}] {flight.departure_city.name} - {flight.arrival_city.name}", # [민석항공] 김포 - 제주
                            "travel_date": datetime.date(flight.departure_time),
                            "logo": flight.aircraft.airline.logo,
                        }
                        for flight in flights
                    ],
                    "total_price": order.total_price,
                    "number_of_tickets": order.number_of_tickets,
                    "payments_method": order.payments_method,
                }
            )

        result = {
            "type": "order_list",
            "data": data
        }

        return JsonResponse({"result": result}, status=200)
