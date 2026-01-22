from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from .models import Fish, Catch
from .forms import CatchForm

User = get_user_model()


class FishSpeciesCreationTestCase(TestCase):
    """Test cases for creating new fish species when logging a catch."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testangler", password="testpass123"
        )
        self.existing_fish = Fish.objects.create(
            official_name="Bass",
            identifying_characteristics="Striped body",
            preferred_baits_lures="Worms, small fish",
            best_fishing_method="Casting",
            preferred_environments="Lakes, rivers",
        )

    def test_catch_form_requires_fish_or_new_species(self):
        """Test that form requires either existing fish or new species."""
        form_data = {
            "length": Decimal("25.5"),
            "length_unit": "cm",
            "weight": Decimal("1.5"),
            "weight_unit": "kg",
            "catch_location": "Lake Michigan",
            "catch_datetime": timezone.now(),
            "released": True,
            "is_public": True,
        }
        form = CatchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Please select an existing fish species", str(form.errors))

    def test_catch_form_accepts_existing_fish(self):
        """Test that form accepts existing fish species."""
        form_data = {
            "fish": self.existing_fish.id,
            "length": Decimal("25.5"),
            "length_unit": "cm",
            "weight": Decimal("1.5"),
            "weight_unit": "kg",
            "catch_location": "Lake Michigan",
            "catch_datetime": timezone.now(),
            "released": True,
            "is_public": True,
        }
        form = CatchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_catch_form_accepts_new_fish_species(self):
        """Test that form accepts new fish species."""
        form_data = {
            "new_fish_species": "Pike",
            "length": Decimal("30.0"),
            "length_unit": "cm",
            "weight": Decimal("2.0"),
            "weight_unit": "kg",
            "catch_location": "Lake Superior",
            "catch_datetime": timezone.now(),
            "released": True,
            "is_public": True,
        }
        form = CatchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_catch_form_rejects_both_fish_and_new_species(self):
        """Test that form rejects both existing and new species being filled."""
        form_data = {
            "fish": self.existing_fish.id,
            "new_fish_species": "Pike",
            "length": Decimal("25.5"),
            "length_unit": "cm",
            "weight": Decimal("1.5"),
            "weight_unit": "kg",
            "catch_location": "Lake Michigan",
            "catch_datetime": timezone.now(),
            "released": True,
            "is_public": True,
        }
        form = CatchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("either select an existing", str(form.errors))

    def test_log_catch_creates_new_fish_species(self):
        """Test that log_catch view creates a new fish species."""
        self.client.login(username="testangler", password="testpass123")
        catch_data = {
            "new_fish_species": "Trout",
            "length": "22.5",
            "length_unit": "cm",
            "weight": "1.2",
            "weight_unit": "kg",
            "catch_location": "Rocky Stream",
            "catch_datetime": timezone.now().isoformat(),
            "released": True,
            "is_public": True,
        }
        response = self.client.post("/log-catch/", catch_data)

        # Check that the response redirects to profile
        self.assertEqual(response.status_code, 302)

        # Check that the new fish species was created
        self.assertTrue(Fish.objects.filter(official_name="Trout").exists())

        # Check that the catch was created with the new species
        trout = Fish.objects.get(official_name="Trout")
        catch = Catch.objects.filter(user=self.user, fish=trout).first()
        self.assertIsNotNone(catch)

    def test_log_catch_with_existing_fish(self):
        """Test that log_catch view works with existing fish species."""
        self.client.login(username="testangler", password="testpass123")
        catch_data = {
            "fish": self.existing_fish.id,
            "length": "25.5",
            "length_unit": "cm",
            "weight": "1.5",
            "weight_unit": "kg",
            "catch_location": "Lake Michigan",
            "catch_datetime": timezone.now().isoformat(),
            "released": True,
            "is_public": True,
        }
        response = self.client.post("/log-catch/", catch_data)

        # Check that the response redirects to profile
        self.assertEqual(response.status_code, 302)

        # Check that the catch was created
        catch = Catch.objects.filter(user=self.user, fish=self.existing_fish).first()
        self.assertIsNotNone(catch)

    def test_duplicate_fish_species_not_created(self):
        """Test that duplicate fish species are not created using get_or_create."""
        fish_count_before = Fish.objects.count()
        self.client.login(username="testangler", password="testpass123")

        # Log two catches with the same new fish species
        catch_data_1 = {
            "new_fish_species": "Salmon",
            "length": "35.0",
            "length_unit": "cm",
            "weight": "3.0",
            "weight_unit": "kg",
            "catch_location": "River",
            "catch_datetime": timezone.now().isoformat(),
            "released": True,
            "is_public": True,
        }
        self.client.post("/log-catch/", catch_data_1)

        catch_data_2 = {
            "new_fish_species": "Salmon",
            "length": "32.0",
            "length_unit": "cm",
            "weight": "2.8",
            "weight_unit": "kg",
            "catch_location": "River",
            "catch_datetime": timezone.now().isoformat(),
            "released": True,
            "is_public": True,
        }
        self.client.post("/log-catch/", catch_data_2)

        # Check that only one Salmon species was created
        fish_count_after = Fish.objects.count()
        self.assertEqual(fish_count_after - fish_count_before, 1)
        self.assertEqual(Catch.objects.filter(fish__official_name="Salmon").count(), 2)
