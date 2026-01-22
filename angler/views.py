from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home(request):
    """Default view for angler app. Prompts login or registration if not authenticated."""
    if request.user.is_authenticated:
        return render(request, "angler/home.html")
    return render(request, "angler/welcome.html")


@login_required
def profile(request):
    """Display the authenticated user's profile page."""
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


@login_required
def log_catch(request):
    """Display the form to log a new catch."""
    from .forms import CatchForm
    from .models import Fish

    if request.method == "POST":
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
    else:
        form = CatchForm()
    return render(request, "angler/log_catch.html", {"form": form})
