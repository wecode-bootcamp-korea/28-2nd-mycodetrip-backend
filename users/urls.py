from django.urls import path

from users.views import AuthorizationView, UserOrderView

urlpatterns = [
    path("/authorize", AuthorizationView.as_view()),
    path("/orders", UserOrderView.as_view()),
]
