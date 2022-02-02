import pytz
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.views import View
from django.db.models import Q, Min

from flights.models import Flight, FlightSeat, Airline, City, Category, Seat, Thumbnail

class FlightListView(View):
    def get(self, request):
        KST = pytz.timezone('Asia/Seoul')
        MAX_PRICE = 99999999

        # 필수 쿼리파라미터
        try:
            departure_date = request.GET["departure_date"] # "2022-02-27"
            arrival_date   = request.GET["arrival_date"]
            departure_city = request.GET["departure_city"]
            arrival_city   = request.GET["arrival_city"]

            # 선택 쿼리파라미터
            airline_list = request.GET.getlist("airline_list")# ['1', '2', '']
            at_time      = request.GET.getlist("at_time") # ['0','6','12','18'], 없을땐 [] 빈리스트 반환
            seat_type    = request.GET.getlist("seat_type")
            sorting      = request.GET.get("sorting", "lower_price") # sorting=''
            max_price    = request.GET.get("max_price", None)
            offset       = int(request.GET.get("offset", 0))
            limit        = int(request.GET.get("limit", 20))

            # timezone 정보 포함한 aware datetime 객체
            year, month, day = map(int,departure_date.split("-"))
            aware_datetime = datetime(year,month,day, tzinfo=KST)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        if '' in airline_list:
            airline_list.remove('')

        if '' in at_time:
            at_time.remove('')

        if '' in seat_type:
            seat_type.remove('')

        if sorting == '':
            sorting = "lower_price"

        if max_price == '':
            max_price=MAX_PRICE


        time_set = {
            0: aware_datetime,
            6: aware_datetime+timedelta(hours=6),
            12: aware_datetime+timedelta(hours=12),
            18: aware_datetime+timedelta(hours=18),
            24: aware_datetime+timedelta(hours=24)
        }

        sort_set = {
            "lower_price"      : "flightseat__price", # 테이블명 소문자
            "earlier_departure": "departure_time",
            "late_departure"   : "-departure_time",
        }

        q = Q()
        q &= Q(departure_city__name=departure_city, arrival_city__name=arrival_city)
        q &= Q(departure_time__range=(time_set[0], time_set[24]))

        if at_time:
            time_q = Q()
            if '0' in at_time:
                time_q |= Q(departure_time__range=(time_set[0], time_set[6]))
            if '6' in at_time:
                time_q |= Q(departure_time__range=(time_set[6], time_set[12]))
            if '12' in at_time:
                time_q |= Q(departure_time__range=(time_set[12], time_set[18]))
            if '18' in at_time:
                time_q |= Q(departure_time__range=(time_set[18], time_set[24]))

            q &= time_q

        if airline_list:
            q &= Q(aircraft__airline__id__in=airline_list)
        if seat_type:
            q &= Q(flightseat__seat_id__in=seat_type)
        if max_price:
            q &= Q(flightseat__price__lte=int(max_price))

        flights_query = Flight.objects.filter(q).order_by(sort_set[sorting])
        flights = flights_query.select_related("departure_city","arrival_city","aircraft")[offset:offset+limit]

        try:
            result = {
                "total": flights_query.count(), # 총 항공편 개수
                "departure_date": departure_date,
                "arrival_date": arrival_date,
                "type": "flight_list",
                "data": [{
                    "id": FlightSeat.objects.get(flight=flight).id, # FIXME 에러날 위험?
                    "flight_time": flight.flight_time, # 비행 시간
                    "airline"    : flight.aircraft.airline.name, # 항공사
                    "aircraft"   : flight.aircraft.code, # 항공기
                    "logo"       : flight.aircraft.airline.logo,
                    "price"      : int(FlightSeat.objects.get(flight=flight, seat=seat).price),
                    "tickets"    : FlightSeat.objects.get(flight=flight).stock, # 구매 가능한 티켓 수
                    "seat_type"  : FlightSeat.objects.get(flight=flight).seat.type, # 좌석 등급
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
                } for flight in flights for seat in flight.seats.all()],
            }
            return JsonResponse({"result":result}, status=200)

        except FlightSeat.DoesNotExist:
            return JsonResponse({"message":"FLIGHTSEAT_DOES_NOT_EXIST"}, status=400)



class FlightDetailView(View):
    def get(self, request):
        try:
            # id 값을 통해서 예약 페이지 항공편 조회
            departure_flight = request.GET["departure_flight"] # pk = 1332
            return_flight    = request.GET["return_flight"]

            flight_seats = FlightSeat.objects.filter(Q(id=departure_flight)|Q(id=return_flight)).order_by("flight__departure_time")

            result = {
                "type": "selected_flights",
                "data":[{
                    "id": flight_seat.id,
                    "flight_time": flight_seat.flight.flight_time,
                        "airline"    : flight_seat.flight.aircraft.airline.name,
                        "aircraft"   : flight_seat.flight.aircraft.code,
                        "logo"       : flight_seat.flight.aircraft.airline.logo,
                        "price"      : flight_seat.price,
                        "seat_type"  : flight_seat.seat.type,
                        "departure": {
                            "time": flight_seat.flight.departure_time,
                            "city": flight_seat.flight.departure_city.name,
                            "code": flight_seat.flight.departure_city.code,
                        },
                        "arrival": {
                            "time": flight_seat.flight.arrival_time,
                            "city": flight_seat.flight.arrival_city.name,
                            "code": flight_seat.flight.arrival_city.code,
                        },
                } for flight_seat in flight_seats]
            }
            return JsonResponse({"result":result}, status=200)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

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

class MainView(View):
    def get(self, request):
        city = request.GET.get("city")
        offset = request.GET.get("offset", 0)
        limit = request.GET.get("limit", 4)

        flights= Flight.objects.annotate(min_price = Min("flightseat__price")).filter(arrival_city__name = city)

        result = {
            "city" : city,
            "data" : [{
                "id"             : flight.id,
                "image"          : Thumbnail.objects.filter(city_id=flight.arrival_city.id).order_by("?").first().image,
                "departure_city" : flight.departure_city.name,
                "arrival_city"   : flight.arrival_city.name,
                "departure_time" : flight.departure_time,
                "arrival_time"   : flight.arrival_time,
                "price"          : int(flight.min_price)
           } for flight in flights.order_by("min_price")[offset:offset+limit]]}

        return JsonResponse({"result": result}, status=200)
