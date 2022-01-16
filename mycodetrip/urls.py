from django.urls import path, include

urlpatterns = [
    path("flights", include("flights.urls")),
    path("users", include("users.urls")),
]
