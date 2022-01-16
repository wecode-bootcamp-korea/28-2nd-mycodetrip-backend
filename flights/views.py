import pytz
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from flights.models import Flight, FlightSeat, Airline, City, Category, Seat


class FlightListView(View):
    def get(self, request):
        # 필수 쿼리파라미터
        try:
            departure_date = request.GET["departure_date"] # "2022-02-27"
            arrival_date   = request.GET["arrival_date"]
            departure_city = request.GET["departure_city"]
            arrival_city   = request.GET["arrival_city"]
        except KeyError:
            return JsonResponse({"message":"REQUIRED_PARAMETER_MISSING"})

        # 선택 쿼리파라미터
        airline_list = request.GET.getlist("airline_list")
        at_time      = request.GET.getlist("at_time") # ['0','6','12','18'], 없을땐 [] 빈리스트 반환
        seat_type    = request.GET.getlist("seat_type")
        sorting      = request.GET.get("sorting", "lower_price")
        max_price    = request.GET.get("max_price", None)
        offset       = int(request.GET.get("offset", 0))
        limit        = int(request.GET.get("limit", 20))

        # timezone 정보 포함한 aware datetime 객체
        KST = pytz.timezone('Asia/Seoul')
        year, month, day = map(int,departure_date.split("-"))
        aware_datetime = datetime(year,month,day, tzinfo=KST)

        TIME = {
            0: aware_datetime,
            6: aware_datetime+timedelta(hours=6),
            12: aware_datetime+timedelta(hours=12),
            18: aware_datetime+timedelta(hours=18),
            24: aware_datetime+timedelta(hours=24)
        }

        SORT = {
            "lower_price"      : "flightseat__price", # 테이블명 소문자
            "earlier_departure": "departure_time",
            "late_departure"   : "-departure_time",
        }

        try:
            from_city = City.objects.get(name=departure_city)
            to_city   = City.objects.get(name=arrival_city)
        except City.DoesNotExist:
            return JsonResponse({"message":"INVALID_CITY"}, status=400)

        '''
        <SQL>
        SELECT * FROM flights
        WHERE
            departure_city_id = 2 AND
            arrival_city=3 AND
            (
                departure_time between time[0] AND time[6] OR
                departure_time between time[12] AND time[18]
            );
        '''

        q = Q()
        q &= Q(departure_city=from_city.id, arrival_city=to_city.id)
        q &= Q(departure_time__range=(TIME[0], TIME[24]))

        if at_time:
            time_q = Q()

            if '0' in at_time:
                time_q |= Q(departure_time__range=(TIME[0], TIME[6]))
            if '6' in at_time:
                time_q |= Q(departure_time__range=(TIME[6], TIME[12]))
            if '12' in at_time:
                time_q |= Q(departure_time__range=(TIME[12], TIME[18]))
            if '18' in at_time:
                time_q |= Q(departure_time__range=(TIME[18], TIME[24]))

            q &= time_q

        try:
            airline_list = [int(airline) for airline in airline_list]
            seat_type = [int(type) for type in seat_type]
            if max_price:
                max_price = int(max_price)
        except ValueError:
            return JsonResponse({"message":"INVALID_INPUT"}, status=400)


        if airline_list:
            q &= Q(aircraft__airline__id__in=airline_list)
        if seat_type:
            q &= Q(flightseat__seat_id__in=seat_type)
        if max_price:
            q &= Q(flightseat__price__lte=max_price)

        flights_query = Flight.objects.filter(q).order_by(SORT[sorting])
        flights = flights_query.select_related("departure_city","arrival_city","aircraft")[offset:offset+limit]

        try:
            result = {
                "total": flights_query.count(), # 총 항공편 개수
                "departure_date": departure_date,
                "arrival_date": arrival_date,
                "type": "flight_list",
                "data": [{
                    "id": flight.id, # 항공편 pk
                    "flight_time": flight.flight_time, # 비행 시간
                    "airline"    : flight.aircraft.airline.name, # 항공사
                    "aircraft"   : flight.aircraft.code, # 항공기
                    "logo"       : flight.aircraft.airline.logo,
                    "price"      : int(FlightSeat.objects.get(flight=flight).price),
                    "tickets"    : FlightSeat.objects.get(flight=flight).stock, # 구매 가능한 티켓 수
                    "seat_type"  : FlightSeat.objects.get(flight=flight).seat_id, # 좌석 등급
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

        except FlightSeat.DoesNotExist:
            return JsonResponse({"message":"FLIGHTSEAT_DOES_NOT_EXIST"}, status=400)

class CityListView(View):
    def get(self, request):
        categories = Category.objects.all()
        result = {
            "type": "city_list",
            "data":[{
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
            "type": "airline_list",
            "data": [{
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
            "type": "seat_type",
            "data": [{
                "id"  : seat.id,
                "name": seat.type,
            } for seat in seats],
        }
        return JsonResponse({"result":result}, status=200)
