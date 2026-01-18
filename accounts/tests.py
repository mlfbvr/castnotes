from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


class UserRegistrationTest(TestCase):
    """
    Test cases for the user registration process.
    Covers successful registration, password mismatch, and duplicate email scenarios.
    """

    def test_register_user_success(self):
        """
        User can register successfully with valid data.
        """
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "full_name": "Test User",
                "password": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(CustomUser.objects.filter(username="testuser").exists())

    def test_register_user_password_mismatch(self):
        """
        Registration fails if passwords do not match.
        """
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser2",
                "email": "testuser2@example.com",
                "full_name": "Test User2",
                "password": "testpass123",
                "password2": "wrongpass",
            },
        )
        self.assertContains(response, "Passwords do not match")
        self.assertFalse(CustomUser.objects.filter(username="testuser2").exists())

    def test_register_user_duplicate_email(self):
        """
        Registration fails if the email is already in use.
        """
        CustomUser.objects.create_user(
            username="existing",
            email="dupe@example.com",
            password="pass",
            full_name="Existing User",
        )
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser3",
                "email": "dupe@example.com",
                "full_name": "Test User3",
                "password": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertContains(response, "Email already in use")
        self.assertFalse(CustomUser.objects.filter(username="testuser3").exists())
