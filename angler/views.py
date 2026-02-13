from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from angler.models import Catch, FishingSession
from datetime import datetime
from angler.utils import get_lat_long, get_weather_for_location


class HomeView(TemplateView):
    """Default view for angler app. Prompts login or registration if not authenticated."""

    def get_context_data(self, **kwargs):
        active_fishing_session = None
        if self.request.user.is_authenticated:
            active_fishing_session = FishingSession.objects.filter(
                user=self.request.user, end_datetime__isnull=True
            ).first()
        context = super().get_context_data(**kwargs)
        context["active_fishing_session"] = active_fishing_session
        try:
            latitude, longitude = (
                get_lat_long(active_fishing_session.location)
                if active_fishing_session
                else (None, None)
            )
        except ValueError as e:
            print(f"Error parsing location: {e}")
            latitude, longitude = None, None

        context["active_fishing_session_location"] = (
            {
                "latitude": latitude or 0,
                "longitude": longitude or 0,
            }
            if active_fishing_session
            else None
        )
        context["user"] = self.request.user
        return context

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return "angler/home.html"
        return "angler/welcome.html"


class ProfileView(LoginRequiredMixin, View):
    """Display the authenticated user's profile page."""

    def get(self, request):
        catches = request.user.catches.all().order_by("-catch_datetime")[:5]
        return render(
            request,
            "angler/profile.html",
            {
                "user": request.user,
                "total_catches_count": request.user.catches.all().count(),
                "catches": catches,
            },
        )


class LogCatchView(LoginRequiredMixin, View):
    """Display the form to log a new catch."""

    def post(self, request):
        from .forms import CatchForm
        from .models import Fish

        form = CatchForm(request.POST, request.FILES)
        if form.is_valid():
            new_fish_species = form.cleaned_data.get("new_fish_species")

            # Create a new fish species if provided
            if new_fish_species:
                fish, _ = Fish.objects.get_or_create(
                    official_name=new_fish_species,
                    defaults={
                        "identifying_characteristics": "User-created entry",
                        "preferred_baits_lures": "Not specified",
                        "best_fishing_method": "Not specified",
                        "preferred_environments": "Not specified",
                    },
                )
            else:
                fish = form.cleaned_data.get("fish")

            # Get the fishing session if provided
            session_uuid = form.cleaned_data.get("session_uuid")
            session = None
            if session_uuid:
                session = FishingSession.objects.filter(
                    user=request.user, uuid=session_uuid
                ).first()

            try:
                catch = form.save(
                    commit=False
                )  # Create the catch instance without saving to database
                catch.user = request.user  # Assign the current user to the catch
                catch.fish = fish  # Assign the fish (new or existing) to the catch
                catch.session = (
                    session  # Assign the fishing session to the catch if available
                )
                catch.save()  # Save the catch to the database

                # Render the log_new_catch partial with success message
                return render(
                    request,
                    "angler/partials/log_new_catch.html",
                    {"form": form, "time": datetime.now()},
                )
            except Exception as e:
                # Catch any database or other errors during catch creation
                # Log the error for debugging purposes
                error_message = f"Failed to log catch: {str(e)}"
                print(error_message)

                # Render the log_new_catch partial with error message
                return render(
                    request,
                    "angler/partials/log_new_catch.html",
                    {"form": form, "time": datetime.now(), "error": error_message},
                )
        else:
            # Form is invalid, render the partial with form errors
            return render(
                request,
                "angler/partials/log_new_catch.html",
                {
                    "form": form,
                    "time": datetime.now(),
                    "error": "Please correct the errors below.",
                },
            )

    def get(self, request):
        from .forms import CatchForm

        active_fishing_session = FishingSession.objects.filter(
            user=request.user, end_datetime__isnull=True
        ).first()

        # Include the active fishing session in the context of the form
        form = CatchForm(
            initial={
                "session_uuid": (
                    active_fishing_session.uuid if active_fishing_session else None
                ),
                "catch_location": (
                    active_fishing_session.location if active_fishing_session else ""
                ),
                "catch_datetime": datetime.now(),
            }
        )
        try:
            latitude, longitude = (
                get_lat_long(active_fishing_session.location)
                if active_fishing_session
                else (None, None)
            )
        except ValueError:
            latitude, longitude = None, None

        active_fishing_session_location = (
            {
                "latitude": latitude or 0,
                "longitude": longitude or 0,
            }
            if active_fishing_session
            else None
        )
        return render(
            request,
            "angler/log_catch.html",
            {
                "form": form,
                "active_fishing_session_location": active_fishing_session_location,
            },
        )


class CatchDetailsView(LoginRequiredMixin, DetailView):
    """
    View to display details of a specific catch.
    Only accessible to the user who logged the catch.
    Will return an empty queryset if the catch does not exist or does not belong to the user.
    """

    model = Catch
    template_name = "angler/catch_details.html"
    context_object_name = "catch"
    allow_empty = True

    def get_object(self, queryset=None):
        """
        Retrieve the catch object if it belongs to the logged-in user.
        Return None if the catch does not exist or does not belong to the user.
        """

        catch = Catch.objects.get(user=self.request.user, pk=self.kwargs.get("pk"))

        try:
            latitude, longitude = (
                get_lat_long(catch.catch_location)
                if catch and catch.catch_location
                else (None, None)
            )
        except ValueError:
            latitude, longitude = None, None
        try:
            # print the deconstructed catch for debugging purposes
            return {
                "catch": catch,
                "location": {
                    "latitude": latitude or 0,
                    "longitude": longitude or 0,
                },
            }
        except Catch.DoesNotExist:
            return None


class CreateFishingSessionView(LoginRequiredMixin, View):
    """View to display details of a specific fishing session."""

    model = FishingSession

    def get(self, request):
        from .forms import FishingSessionForm

        active_fishing_session = FishingSession.objects.filter(
            user=request.user, end_datetime__isnull=True
        ).first()
        if active_fishing_session:
            return redirect("profile")
        form = FishingSessionForm()
        return render(request, "angler/fishing_session.html", {"form": form})

    def post(self, request):
        from .forms import FishingSessionForm
        from datetime import datetime

        form = FishingSessionForm(request.POST)
        if form.is_valid():
            try:
                session = form.save(
                    commit=False
                )  # Create session instance without saving to database
                session.user = request.user  # Assign the current user to the session
                session.start_datetime = (
                    datetime.now()
                )  # Set the session start time to now
                session.save()  # Attempt to save the session to the database

                # Redirect to the session details page using the generated UUID
                return redirect("session-details", uuid=session.uuid)
            except Exception as e:
                # Catch any database or other errors during session creation
                # Log the error for debugging purposes
                error_message = f"Error creating fishing session: {str(e)}"
                print(error_message)

                # Re-render the form with error message for user feedback
                form.add_error(
                    None, "Failed to create fishing session. Please try again."
                )
                return render(
                    request,
                    "angler/fishing_session.html",
                    {"form": form, "error": error_message},
                )


class FishingSessionDetailsView(LoginRequiredMixin, DetailView):
    """View to display the current active fishing session."""

    model = FishingSession
    template_name = "angler/session_details.html"
    context_object_name = "fishing_session"
    catches = None

    def get_object(self, queryset=None):
        """Retrieve the active fishing session for the logged-in user."""
        #
        # Get the fishes caught during this session
        fishing_session = FishingSession.objects.filter(
            user=self.request.user, uuid=self.kwargs.get("uuid")
        ).first()
        catches = (
            Catch.objects.filter(session=fishing_session) if fishing_session else None
        )
        try:
            latitude, longitude = (
                get_lat_long(fishing_session.location)
                if fishing_session
                else (None, None)
            )
        except ValueError:
            latitude, longitude = None, None

        return {
            "fishing_session": fishing_session,
            "location": (
                {
                    "latitude": latitude or 0,
                    "longitude": longitude or 0,
                }
                if fishing_session
                else None
            ),
            "catches": catches,
        }


class ListFishingSessionsView(LoginRequiredMixin, View):
    """View to list all fishing sessions of the logged-in user."""

    def get(self, request):
        sessions = FishingSession.objects.filter(user=request.user).order_by(
            "-start_datetime"
        )

        return render(
            request,
            "angler/sessions_list.html",
            {
                "sessions": sessions,
            },
        )


class EndFishingSessionView(LoginRequiredMixin, View):
    """View to end an active fishing session."""

    def post(self, request, pk):
        from datetime import datetime
        from django.shortcuts import get_object_or_404

        fishing_session = get_object_or_404(
            FishingSession, pk=pk, user=request.user, end_datetime__isnull=True
        )
        fishing_session.end_datetime = datetime.now()
        fishing_session.save()
        return redirect("session-details", uuid=fishing_session.uuid)


class CurrentWeatherConditionsView(LoginRequiredMixin, View):
    """View to fetch and display current weather conditions for a given location."""

    def get(self, request):

        location = request.GET.get("catch_location")
        form_only = request.GET.get("form", "false").lower() == "true"
        if not location:
            return render(
                request,
                "angler/partials/weather_info.html",
                {"error": "No location provided."},
            )

        try:
            weather_data = get_weather_for_location(location)

            if form_only:
                return render(
                    request,
                    "angler/partials/weather_info.html",
                    {"weather_data": weather_data, "form": form_only},
                )
            else:
                return render(
                    request,
                    "angler/partials/weather_info.html",
                    {"weather_data": weather_data},
                )
        except Exception as e:
            error_message = f"Error fetching weather data: {str(e)}"
            print(error_message)
            return render(
                request,
                "angler/partials/weather_info.html",
                {"error": "Failed to fetch weather data. Please try again."},
            )
