import imp
from django.urls import path

from users.views import AuthorizationView

urlpatterns = [
    path("/authorize", AuthorizationView.as_view()),
]
