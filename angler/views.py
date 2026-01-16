
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
	"""Default view for angler app. Prompts login or registration if not authenticated."""
	if request.user.is_authenticated:
		return render(request, "angler/home.html")
	return render(request, "angler/welcome.html")
