from datetime import datetime, timedelta
from django.http import JsonResponse

from django.views import View
from django.db.models import Q

from flights.models import *


class FlightListView(View):
    def get(self, request):
        # 필수 쿼리파라미터
        departure_date   = request.GET.get("departure_date") # 여행 시작
        arrival_date     = request.GET.get("arrival_date") # 여행 끝
        departure_city   = request.GET.get("departure_city") # "김포"
        arrival_city     = request.GET.get("arrival_city") # "제주"
        is_round_trip    = request.GET.get("is_round_trip") # 왕복?
        number_of_person = request.GET.get("number_of_person") # 성인 1 명
        # 선택 쿼리파라미터
        airline_id_list  = request.GET.getlist("airline", "all") # 항공사 [1,3,4]
        at_time          = request.GET.getlist("during_time", "all") # 00:00~06:00 => [0,6,12,18]
        seat_type        = request.GET.getlist("seat_type", "all") # 좌석 등급
        sorting          = request.GET.get("sort", "낮은가격순")
        print(departure_city)
        print(arrival_city)
        sort = {
            "낮은가격순":"price",
            # "출발시간빠른순":"departure_time",
            # "출발시간느린순":"-departure_time",
        }

        # departure_date = str(datetime.strptime(departure_date, "%Y-%m-%d")) # 2022-02-14
        # arrival_date   = str(datetime.strptime(arrival_date, "%Y-%m-%d"))

        from_city = City.objects.filter(name=departure_city).first()
        to_city   = City.objects.filter(name=arrival_city).first()

        q = Q()
        q &= Q(departure_time__gte=departure_date, departure_city=from_city.id, arrival_city=to_city.id)

        if airline_id_list:
            pass
        if at_time:
            pass
        if seat_type:
            pass

        flights = Flight.objects.filter(q).select_related("departure_city","arrival_city","aircraft")

        result = {
            "total": flights.count(),
            "departure_date": departure_date,
            "arrival_date": arrival_date,
            "flight_list": [{
                "id": flight.id, # 항공편 pk
                "flight_time": flight.flight_time, # 비행 시간
                "airline"    : flight.aircraft.airline.name, # 항공사
                "aircraft"   : flight.aircraft.code, # 항공기
                "logo"       : flight.aircraft.airline.logo,
                "price"      : int(FlightSeat.objects.filter(flight=flight).first().price),
                "tickets"    : FlightSeat.objects.filter(flight=flight).first().stock,
                "seat_type"  : FlightSeat.objects.filter(flight=flight).first().seat_id, # 좌석 등급
                "departure": {
                    "time": flight.departure_time, # 출발 시간
                    "city": flight.departure_city.name, # 출발 도시명
                    "code": flight.departure_city.code, # 출발 도시 코드
                },
                "arrival": {
                    "time": flight.arrival_time, # 도착 시간
                    "city": flight.arrival_city.name, # 도착 도시명
                    "code": flight.arrival_city.code, # 도착 도시 코드
                },
            } for flight in flights],
        }
        return JsonResponse({"result":result}, status=200)

class CityListView(View):
    def get(self, request):

        categories = Category.objects.select_related("city")

        result = {
            "category":[{
                "id": category.id,
                "category": category.name,
                "city": [city for city in category.city_set.values()]
            } for category in categories]
        }
        return JsonResponse({"result":result}, status=200)

class AirlineListView(View):
    def get(self, request):
        airlines = Airline.objects.all()

        result = {
            "airline_list": [{ # 항공사 리스트
                "id": airline.id,
                "name": airline.name,
                "logo": airline.logo,
            } for airline in airlines]
        }
        return JsonResponse({"result":result}, status=200)

class SeatTypeView(View):
    def get(self, request):
        seats = Seat.objects.all()

        result = {
            "seat_list": [{ # 좌석 등급 리스트
                "id"  : seat.id,
                "type": seat.type,
            } for seat in seats],
        }
        return JsonResponse({"result":result}, status=200)
