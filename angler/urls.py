from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="angler-home"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("log-catch/", views.LogCatchView.as_view(), name="log-catch"),
    path("catch/<int:pk>/", views.CatchDetailsView.as_view(), name="catch-details"),
    path("session/", views.ListFishingSessionsView.as_view(), name="fishing-sessions"),
    path(
        "session/new/", views.CreateFishingSessionView.as_view(), name="fishing-session"
    ),
    path(
        "session/<uuid:uuid>/",
        views.FishingSessionDetailsView.as_view(),
        name="session-details",
    ),
    path(
        "session/<int:pk>/end/",
        views.EndFishingSessionView.as_view(),
        name="end-session",
    ),
]
