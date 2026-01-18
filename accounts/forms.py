# Django form definitions for user registration and validation
from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser


class UserRegistrationForm(forms.ModelForm):
    """
    Form for registering a new user account.
    Includes password confirmation and email uniqueness validation.
    """

    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "full_name")  # Required registration fields

    def clean_password2(self):
        """
        Ensure the two entered passwords match.
        """
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def clean_email(self):
        """
        Ensure the email address is unique among all users.
        """
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email already in use")
        return email
