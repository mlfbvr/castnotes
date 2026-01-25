from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from angler.models import Catch


class HomeView(TemplateView):
    """Default view for angler app. Prompts login or registration if not authenticated."""

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

            catch = form.save(commit=False)
            catch.user = request.user
            catch.fish = fish
            catch.save()
            return redirect("profile")

    def get(self, request):
        from .forms import CatchForm

        form = CatchForm()
        return render(request, "angler/log_catch.html", {"form": form})


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
