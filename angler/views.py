
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
	return render(request, "angler/profile.html", {"user": request.user})


@login_required
def log_catch(request):
	"""Display the form to log a new catch."""
	from .forms import CatchForm

	if request.method == "POST":
		form = CatchForm(request.POST, request.FILES)
		if form.is_valid():
			catch = form.save(commit=False)
			catch.user = request.user
			catch.save()
			return redirect("profile")
	else:
		form = CatchForm()
	return render(request, "angler/log_catch.html", {"form": form})
