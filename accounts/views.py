# Views for user registration and account management
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm


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
