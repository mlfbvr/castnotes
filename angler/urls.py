from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="angler-home"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("log-catch/", views.LogCatchView.as_view(), name="log-catch"),
    path("catch/<int:pk>/", views.CatchDetailsView.as_view(), name="catch-details"),
    path("session/", views.CreateFishingSessionView.as_view(), name="fishing-session"),
]
