from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from angler.models import Fish, Catch

User = get_user_model()


class FishModelTestCase(TestCase):
    """Test cases for the Fish model."""

    def setUp(self):
        """Set up test data."""
        self.fish = Fish.objects.create(
            official_name="Largemouth Bass",
            nicknames="Black bass, Florida bass",
            identifying_characteristics="Dark green/black coloring, large mouth",
            preferred_baits_lures="Worms, minnows, crankbaits",
            best_fishing_method="Casting to structures",
            preferred_environments="Lakes, ponds, rivers",
        )

        self.user = User.objects.create_user(
            username="angler1", password="securepassword"
        )

        self.catch = Catch.objects.create(
            user=self.user,
            fish=self.fish,
            length=Decimal("30.5"),
            length_unit="cm",
            weight=Decimal("2.3"),
            weight_unit="kg",
            catch_location="Lake Springfield",
            catch_datetime="2024-06-01T10:00:00Z",
            released=True,
            is_public=True,
        )

    def test_fish_str_representation(self):
        """Test that Fish model returns official name as string representation."""
        self.assertEqual(str(self.fish), "Largemouth Bass")

    def test_fish_creation(self):
        """Test that Fish model can be created and retrieved."""
        retrieved_fish = Fish.objects.get(official_name="Largemouth Bass")
        self.assertEqual(retrieved_fish.nicknames, "Black bass, Florida bass")
        self.assertIn("Dark green", retrieved_fish.identifying_characteristics)


class CatchModelTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.fish = Fish.objects.create(
            official_name="Largemouth Bass",
            nicknames="Black bass, Florida bass",
            identifying_characteristics="Dark green/black coloring, large mouth",
            preferred_baits_lures="Worms, minnows, crankbaits",
            best_fishing_method="Casting to structures",
            preferred_environments="Lakes, ponds, rivers",
        )

        self.user = User.objects.create_user(
            username="angler1", password="securepassword"
        )

        self.catch = Catch.objects.create(
            user=self.user,
            fish=self.fish,
            length=Decimal("30.5"),
            length_unit="cm",
            weight=Decimal("2.3"),
            weight_unit="kg",
            catch_location="Lake Springfield",
            catch_datetime=datetime.fromisoformat("2024-06-01T10:00:00+00:00"),
            released=True,
            is_public=True,
        )

    def test_catch_creation(self):
        """Test that Catch model can be created and linked to Fish."""
        retrieved_catch = Catch.objects.get(fish=self.fish)
        self.assertEqual(retrieved_catch.length, Decimal("30.5"))
        self.assertEqual(retrieved_catch.weight, Decimal("2.3"))
        self.assertEqual(retrieved_catch.catch_location, "Lake Springfield")

    def test_catch_str_representation(self):
        """Test that Catch model string representation works."""
        self.assertEqual(
            str(self.catch),
            f"Catch of {self.fish.official_name} by {self.user.username} on 2024-06-01",
        )
