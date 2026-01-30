from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from angler.models import Fish
from angler.forms import CatchForm


class FishSpeciesFormValidationTestCase(TestCase):
    """Test cases for CatchForm validation with fish species selection."""

    def setUp(self):
        """Set up test data."""
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
