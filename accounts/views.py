# Views for user registration and account management
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm


def login_view(request):
    """
    Handle user login process.
    This view can be customized to use a custom login form if needed.
    For now, it simply redirects to the built-in login view provided by Django.
    """
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            # Log the user in and redirect to the home page
            login(request, form.get_user())
            return redirect("angler-home")
    else:
        form = UserLoginForm()
    return render(request, "registration/login.html", {"form": form})


def register(request):
    """
    Handle user registration process.
    Displays the registration form, validates input, and creates a new user.
    Redirects to login page on success.
    """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Hash the password
            user.save()
            # Optionally log the user in after registration
            # login(request, user)
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "registration/register.html", {"form": form})
