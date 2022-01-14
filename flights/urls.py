from django.urls import path

from flights.views import AirlineListView, CityListView, FlightListView, SeatTypeView


urlpatterns = [
    path("", FlightListView.as_view()),
    path("/cities", CityListView.as_view()),
    path("/airlines", AirlineListView.as_view()),
    path("/seats", SeatTypeView.as_view()),
]
