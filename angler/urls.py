from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="angler-home"),
    path("profile/", views.profile, name="profile"),
    path("log-catch/", views.log_catch, name="log-catch"),
]
