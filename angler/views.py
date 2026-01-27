from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from angler.models import Catch, FishingSession


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

            catch = form.save(commit=False)
            catch.user = request.user
            catch.fish = fish
            catch.session = session
            catch.save()
            return redirect("profile")

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
            }
        )
        return render(
            request,
            "angler/log_catch.html",
            {
                "form": form,
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
        try:
            return Catch.objects.get(user=self.request.user, pk=self.kwargs.get("pk"))
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
            session = form.save(commit=False)
            session.user = request.user
            session.start_datetime = datetime.now()
            session.save()
            return redirect("profile")


class CurrentFishingSessionView(LoginRequiredMixin, DetailView):
    """View to display the current active fishing session."""

    model = FishingSession
    template_name = "angler/session_details.html"
    context_object_name = "fishing_session"
    catches = None

    def get_object(self, queryset=None):
        """Retrieve the active fishing session for the logged-in user."""

        # Get the fishes caught during this session
        fishing_session = FishingSession.objects.filter(
            user=self.request.user, end_datetime__isnull=True
        ).first()
        catches = (
            Catch.objects.filter(session=fishing_session) if fishing_session else None
        )

        return {
            "fishing_session": fishing_session,
            "catches": catches,
        }
