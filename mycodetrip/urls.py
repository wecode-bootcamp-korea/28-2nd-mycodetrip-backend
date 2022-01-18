from django.urls import path, include

urlpatterns = [
    path('flights', include('flights.urls')),
    path('orders', include('orders.urls'))
]
