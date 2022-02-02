from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

urlpatterns = [
    path("flights", include("flights.urls")),
    path("users", include("users.urls")),
    path("orders", include("orders.urls"))
]

urlpatterns += staticfiles_urlpatterns()
